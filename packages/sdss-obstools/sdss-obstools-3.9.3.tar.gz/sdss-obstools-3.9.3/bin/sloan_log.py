#!/usr/bin/env python3
"""sloan_log.py

A script to automate the bulk of logging and to replace various tools
 like log function, log support, list_ap, list_m, and more. This code is
 entirely dependent on raw images, and their headers, unlike Log Function
 which is dependent on callbacks it catches while open only and is subject to
 crashes. It's inspired by some outputs from time tracking, but it avoids the
 sdss python module and platedb

The intent of this is to create a more future-proof tool for logging through
Sloan V

In order to run it locally, you will need to either have access to /data, or
 fake it with a single night. You'll need a date from /data/spectro and
 /data/apogee/archive. You'll also need setup local forwarding for InfluxDB
"""
import argparse
import multiprocessing
import sys
import textwrap
import warnings
import fitsio

import numpy as np
try:
    from bin import m4l, telescope_status, get_dust
except ImportError as e:
    raise ImportError('Please add ObserverTools/bin to your PYTHONPATH:'
                      '\n    {}'.format(e))
from pathlib import Path
from tqdm import tqdm
from astropy.time import Time

from sdssobstools import apogee_data, log_support, boss_data, sdss_paths

from bin import sjd

if sys.version_info.major < 3:
    raise Exception('Interpretter must be python 3.5 or newer')

# For astropy
warnings.filterwarnings('ignore', category=UserWarning, append=True)
# For numpy boolean arrays
warnings.filterwarnings('ignore', category=FutureWarning, append=True)

__version__ = '3.7.5'

ap_dir = sdss_paths.ap_archive
b_dir = sdss_paths.boss


class Logging:
    """
    A tool to produce a ton of various outputs used for logging. This tool uses
    the images in the /data directory and epics to build a nightlog that doesn't
    require STUI output. It is best run as follow:

    log = Logging(ap_images, b_images, args)
    log.parse_images()
    log.sort()
    log.count_dithers()
    log.p_summary()
    log.p_data()
    log.p_boss()
    log.p_apogee()
    log.log_support()

    or via command line as

    ./sloan_log.py -pt

    or for a previous date

    ./sloan_log.py -pm 59011

    """

    def __init__(self, ap_images, m_images, args):
        self.ap_images = ap_images
        self.b_images = m_images
        self.args = args
        # Dictionary keys that begin with c are of len(carts_in_a_night),
        # keys that begin with i are of len(images_in_a_night), keys that begin
        # with d are of len(dome_flats) (which is not always the same as carts,
        # keys that begin with a are of len(apogee_arcs), which is usually 4 in
        # a full night (morning and evening cals), keys that begin with h are of
        # len(hartmanns), which is usually a few longer than len(carts). Each
        # first letter is used to choose which sorting key to use. There must be
        # a Time key for each new letter, and a new sorter argument must be
        # added to self.sort. All of these dictionary items begin as lists,
        # and are converted to np.arrays or astropy.time.Times in self.sort.
        self.data = {'dField': [], 'dTime': [], 'dConfig': [], 'cLead': [],
                     "dDesign": [], "dTimes": []}
        self.ap_data = {'dDesign': [], "dConfig": [], 'dTime': [],
                        'iTime': [], 'iID': [],
                        'iSeeing': [], 'iDetector': [], 'iDither': [],
                        'iNRead': [], 'iEType': [], 'iDesign': [],
                        "iDesign": [], "iConfig": [],
                        'fDesign': [], 'fTime': [], 'fMissing': [], 'fFaint': [],
                        'fNMissing': [], 'fNFaint': [], 'fRatio': [], 'aTime': [],
                        'aOffset': [], 'aID': [], 'aLamp': [], 'oTime': [],
                        'oOffset': [], 'oDither': [], "dField": [],
                        "iField": [], "fField": []}
        self.b_data = {'dDesign': [], "dConfig": [], 'dTime': [], "dField": [],
                       'iTime': [], 'iID': [],
                       'iDetector': [], 'iDither': [],
                       'iEType': [], 'idt': [], 'iField': [], 'iHart': [],
                       'iDesign': [], "iConfig": [], 'hTime': [],
                       "hField": []}
        # These values are not known from the header and must be created
        # after self.sort. N for number, AP or B for APOGEE or BOSS, and NSE
        # for BOSS dithers, and AB for APOGEE dithers, dt for boss exposure
        # time, since some boss carts use shorter exposures. All these are
        # combined to fill Summary in self.count_dithers
        self.design_data = {'dNAPA': [], 'dNAPB': [], 'dNBN': [], 'dNBS': [],
                            'dNBE': [], 'dNBC': [], 'dBdt': [], 'dNB': [],
                            'dAPSummary': [],
                            'dBSummary': []}
        master_path = (Path(apogee_data.__file__).absolute().parent.parent
                       / "dat/master_dome_flat.fits.gz")
        if not master_path.exists():
            master_path = (Path(apogee_data.__file__).absolute(
            ).parent.parent.parent / "dat/master_dome_flat.fits.gz")
        master_data = fitsio.read(master_path.as_posix())
        self.ap_master = np.median(master_data[:, 550:910], axis=1)
        self.morning_filter = None
        self.ap_image = None
        
        self.support = multiprocessing.Manager().dict()
        self.support["offsets"] = ""
        self.support["focus"] = ""
        self.support["weather"] = ""
        self.support["hartmann"] = ""

    def ap_test(self, img):
        """Calls aptest on hub, this could certainly be replaced in the near
        future.
        """
        # This is from ap_test
        self.args.plot = False
        missing, faint, flux_ratio = img.ap_test((550, 910), self.ap_master)
        if self.args.verbose:
            print('Exposure {}'.format(img.exp_id))
            print(missing, faint)
        n_missing = 0
        n_faint = 0
        for miss in missing:
            if isinstance(miss, bytes) or isinstance(miss, str):
                if 'bundle' in miss:
                    n_missing += 30
                else:
                    n_missing += abs(eval(miss))
            else:
                n_missing += 1
        for fain in faint:
            if isinstance(fain, bytes) or isinstance(fain, str):
                if 'bundle' in fain:
                    n_faint += 30
                else:
                    n_faint += np.abs(eval(fain))
            else:
                n_faint += 1
        # return (n_missing, n_faint, missing, faint, img.cart_id,
        #         img.isot)
        self.ap_data['fNMissing'].append(n_missing)
        self.ap_data['fNFaint'].append(n_faint)
        self.ap_data['fMissing'].append(missing)
        self.ap_data['fFaint'].append(faint)
        self.ap_data['fRatio'].append(flux_ratio)
        self.ap_data['fDesign'].append(img.design_id)
        self.ap_data['fField'].append(img.field_id)
        self.ap_data['fTime'].append(img.isot)

    def parse_images(self):
        """Goes through every image in ap_images and m_images to put them in
        dictionaries."""
        if self.args.apogee:
            print('Reading APOGEE Data ({})'.format(len(self.ap_images)))
            img = None
            for image in tqdm(self.ap_images):
                img = apogee_data.APOGEERaw(image, self.args, 1)
                # img.parse_layer(1)
                if img.lead is None:  # If the first exposure is still
                    # writing, plate_id will be empty and without this if,
                    # it would fail. With this if, it will skip the plate
                    print(f"Skipping {image}")
                    continue
                if (img.exp_type == 'Domeflat') and ('-a-' in img.file.name):
                    self.ap_test(img)
                elif ('Arc' in img.exp_type) and ('-a-' in img.file.name):
                    self.ap_data['aTime'].append(img.isot)
                    self.ap_data['aID'].append(img.exp_id)
                    if 'ThAr' in img.exp_type:
                        self.ap_data['aOffset'].append(
                            img.compute_offset((60, 70), 1105, 40, 1.27))
                        self.ap_data['aLamp'].append('ThAr')
                    elif 'UNe' in img.exp_type:
                        self.ap_data['aOffset'].append(
                            img.compute_offset((60, 70), 1190, 30, 3))
                        self.ap_data['aLamp'].append('UNe')
                    else:
                        print("Couldn't parse the arc image: {} with exposure"
                              " type {}".format(img.file, img.exp_type))
                        self.ap_data["aTime"].pop()
                        self.ap_data["aID"].pop()
                elif ('Object' in img.exp_type) and ('-a-' in img.file.name):
                    # TODO check an object image for a good FWHM (last
                    # input)
                    self.ap_data['oTime'].append(img.isot)
                    self.ap_data['oOffset'].append(
                        # img.compute_offset((30, 35), 1090, 40, 2))
                        img.compute_offset((30, 35), 1100, 40, 2))
                    self.ap_data['oDither'].append(img.dither)

                if img.field_id not in self.data['dField']:
                    self.data['dField'].append(img.field_id)
                    self.data['dDesign'].append(set([img.design_id]))
                    self.data['dConfig'].append(set([img.config_id]))
                    self.data['dTime'].append(img.isot)
                    self.data['dTimes'].append([img.isot])
                    try:
                        self.data['cLead'].append(img.lead)
                    except AttributeError:
                        self.data["cLead"].append("")
                else:
                    i = self.data['dField'].index(img.field_id)
                    # If a design has multiple configs, take the lowest (first)
                    self.data["dDesign"][i].add(img.design_id)
                    self.data["dConfig"][i].add(img.config_id)
                    if img.isot < self.data['dTime'][i]:
                        self.data['dTime'].pop(i)
                        self.data['dTime'].insert(i, img.isot)
                    for i, d in enumerate(self.data["dDesign"]):
                        if d == img.design_id:
                            self.data["dTimes"][i] = min(self.data["dTimes"][i],
                                                         img.isot)
                if img.field_id not in self.ap_data['dField']:
                    self.ap_data['dField'].append(img.field_id)
                    self.ap_data['dDesign'].append(set([img.design_id]))
                    self.ap_data['dConfig'].append(set([img.config_id]))
                    self.ap_data['dTime'].append(img.isot)
                else:
                    i = self.ap_data['dField'].index(img.field_id)
                    self.ap_data["dDesign"][i].add(img.design_id)
                    self.ap_data["dConfig"][i].add(img.config_id)
                    if img.isot < self.ap_data['dTime'][i]:
                        self.ap_data['dTime'].pop(i)
                        self.ap_data['dTime'].insert(i, img.isot)
                detectors = []
                arch_dir = sdss_paths.ap_archive / f"{self.args.sjd}/"
                # red_dir = Path('/data/apogee/quickred/{}/'.format(
                #     self.args.sjd))
                # This used to see if quickred processed, but others preferred
                # to see if the archive image was written
                arch_name = 'apR-a-{}.apz'.format(img.exp_id)
                if (arch_dir / arch_name).exists():
                    detectors.append('a')
                # elif (red_dir / arch_name.replace('1D', '2D')).exists():
                # detectors.append('2')
                else:
                    detectors.append('x')
                if (arch_dir / arch_name.replace('-a-', '-b-')).exists():
                    detectors.append('b')
                # elif (red_dir / arch_name.replace('-a-', '-b-').replace(
                # '1D', '2D')).exists():
                # detectors.append('2')
                else:
                    detectors.append('x')
                if (arch_dir / arch_name.replace('-a-', '-c-')).exists():
                    detectors.append('c')
                # elif (red_dir / arch_name.replace('-a-', '-c-').replace(
                # '1D', '2D')).exists():
                # detectors.append('2')
                else:
                    detectors.append('x')
                self.ap_data['iTime'].append(img.isot)
                self.ap_data['iID'].append(img.exp_id)
                self.ap_data['iSeeing'].append(img.seeing)
                self.ap_data['iDetector'].append('-'.join(detectors))
                self.ap_data['iDither'].append(img.dither)
                self.ap_data['iNRead'].append(img.n_read)
                self.ap_data['iEType'].append(img.exp_type)
                self.ap_data['iDesign'].append(img.design_id)
                self.ap_data["iField"].append(img.field_id)
                self.ap_data['iConfig'].append(img.config_id)
            if img is not None:
                self.ap_image = img
        if self.args.boss:
            print('Reading BOSS Data ({})'.format(len(self.b_images)))
            for image in tqdm(self.b_images):
                img = boss_data.BOSSRaw(image)
                if img.field_id not in self.data['dField']:
                    self.data['dField'].append(img.field_id)
                    self.data['dDesign'].append(set([img.design_id]))
                    self.data['dConfig'].append(set([img.config_id]))
                    self.data['dTimes'].append([img.isot])
                    try:
                        self.data['cLead'].append(img.lead)
                    except AttributeError:
                        self.data["cLead"].append("")
                    self.data['dTime'].append(img.isot)
                else:
                    i = self.data['dField'].index(img.field_id)
                    self.data["dDesign"][i].add(img.design_id)
                    self.data["dConfig"][i].add(img.config_id)
                    if img.isot < self.data['dTime'][i]:
                        self.data['dTime'].pop(i)
                        self.data['dTime'].insert(i, img.isot)
                    for i, d in enumerate(self.data["dDesign"]):
                        if d == img.design_id:
                            self.data["dTimes"][i] = min(self.data["dTimes"][i],
                                                         img.isot)
                            
                if img.field_id not in self.b_data['dField']:
                    self.b_data['dField'].append(img.field_id)
                    self.b_data["dDesign"].append(set([img.design_id]))
                    self.b_data["dConfig"].append(set([img.config_id]))
                    self.b_data['dTime'].append(img.isot)
                else:
                    i = self.b_data['dField'].index(img.field_id)
                    self.b_data["dDesign"][i].add(img.config_id)
                    self.b_data["dConfig"][i].add(img.config_id)
                    if img.isot < self.b_data['dTime'][i]:
                        self.b_data['dTime'].pop(i)
                        self.b_data['dTime'].insert(i, img.isot)
                self.b_data['iTime'].append(img.isot)
                self.b_data['iID'].append(img.exp_id)
                # self.b_data['iSeeing'].append(img.seeing)
                self.b_data['iDither'].append(img.dither)
                self.b_data['iEType'].append(img.flavor)
                self.b_data['idt'].append(img.exp_time)
                self.b_data['iDesign'].append(img.design_id)
                self.b_data['iHart'].append(img.hartmann)
                if img.hartmann == "Left":
                    self.b_data["hTime"].append(img.isot)
                    self.b_data["hField"].append(img.field_id)
                self.b_data['iConfig'].append(img.config_id)
                self.b_data["iField"].append(img.field_id)

                sos_files = []
                # img_mjd = int(Time(img.isot).mjd)
                # All boss exposures write as splog, but manga writes different
                red_dir = sdss_paths.sos / f"{self.args.sjd}"
                red_fil = red_dir / 'splog-r1-{:0>8}.log'.format(img.exp_id)
                try:
                    red_fil.exists()
                except OSError:
                    pass
                if red_fil.exists():
                    sos_files.append('r1')
                else:
                    sos_files.append('xx')
                if (red_fil.parent / red_fil.name.replace('r1', 'b1')).exists():
                    sos_files.append('b1')
                else:
                    sos_files.append('xx')
                if (red_fil.parent / red_fil.name.replace('r1', 'r2')).exists():
                    sos_files.append('r2')
                # else:
                #     m_detectors.append('xx')
                if (red_fil.parent / red_fil.name.replace('r1', 'b2')).exists():
                    sos_files.append('b2')
                # else:
                #     m_detectors.append('xx')
                self.b_data['iDetector'].append('-'.join(sos_files))

    def sort(self):
        """Sorts self.ap_data by design time and by image time and converts to
        arrays"""
        # Data
        for key, item in self.data.items():
            if 'Time' in key and "Times" not in key:
                try:
                    self.data[key] = Time(item)
                except ValueError:
                    self.data[key] = Time(item, format='isot')
            else:
                self.data[key] = np.array(item)
        data_sort = self.data['dTime'].argsort()
        for key, item in self.data.items():
            self.data[key] = item[data_sort]

        if self.args.apogee:
            for key, item in self.ap_data.items():
                if 'Time' in key:
                    try:
                        self.ap_data[key] = Time(item)
                    except ValueError:
                        self.ap_data[key] = Time(item, format='isot')
                    except AttributeError:
                        print(f"Could not read key {key} as time\n"
                              f"{self.ap_data[key]}")
                else:
                    self.ap_data[key] = np.array(item)
            ap_design_sorter = self.ap_data['dTime'].argsort()
            ap_img_sorter = self.ap_data['iTime'].argsort()
            ap_dome_sorter = self.ap_data['fTime'].argsort()
            ap_arc_sorter = self.ap_data['aTime'].argsort()
            ap_obj_sorter = self.ap_data['oTime'].argsort()
            for key, item in self.ap_data.items():
                if key[0] == 'd':
                    self.ap_data[key] = item[ap_design_sorter]
                elif key[0] == 'i':
                    self.ap_data[key] = item[ap_img_sorter]
                elif key[0] == 'f':
                    self.ap_data[key] = item[ap_dome_sorter]
                elif key[0] == 'a':
                    self.ap_data[key] = item[ap_arc_sorter]
                elif key[0] == 'o':
                    self.ap_data[key] = item[ap_obj_sorter]
            if self.args.morning:
                was_dark = False
                prev_time = 0
                lower = None
                for t, reads, exp in zip(self.ap_data['iTime'],
                                         self.ap_data['iNRead'],
                                         self.ap_data['iEType']):
                    if (reads == 60) and (exp == 'Dark'):
                        if was_dark:
                            lower = prev_time
                            break
                        else:
                            was_dark = True
                            prev_time = t
                            if self.args.verbose:
                                print('Morning lower limit: {}'.format(
                                    prev_time))
                    else:
                        was_dark = False
                upper = Time(self.args.sjd + 1, format='mjd')
                if lower is None:
                    raise Exception('Morning cals not completed for this date')
                self.morning_filter = ((lower <= self.ap_data['iTime'])
                                       & (self.ap_data['iTime'] <= upper))

        if self.args.boss:
            for key, item in self.b_data.items():
                if 'Time' in key:
                    try:
                        self.b_data[key] = Time(item)
                    except ValueError:
                        self.b_data[key] = Time(item, format='isot')
                else:
                    self.b_data[key] = np.array(item)
            b_design_sorter = self.b_data['dTime'].argsort()
            b_img_sorter = self.b_data['iTime'].argsort()
            b_h_sorter = self.b_data['hTime'].argsort()
            for key, item in self.b_data.items():
                if key[0] == 'c':
                    self.b_data[key] = item[b_design_sorter]
                elif key[0] == 'i':
                    self.b_data[key] = item[b_img_sorter]
                elif key[0] == 'h':
                    self.b_data[key] = item[b_h_sorter]

    def count_dithers(self):
        for i, field in enumerate(self.data['dField']):
            self.design_data["dNAPA"].append(np.sum(
                (self.ap_data['iField'] == field)
                & (self.ap_data['iDither'] == 'A')
                & (self.ap_data['iEType'] == 'Object')))
            self.design_data["dNAPB"].append(np.sum(
                (self.ap_data['iField'] == field)
                & (self.ap_data['iDither'] == 'B')
                & (self.ap_data['iEType'] == 'Object')))
            self.design_data["dNB"].append(np.sum(
                (self.b_data['iField'] == field)
                & (self.b_data['iEType'] == 'Science')))
            if self.design_data["dNB"][-1] != 0:
                self.design_data["dBdt"].append(np.max(
                    self.b_data['idt'][
                        (self.b_data['iField'] == field)
                        & (self.b_data['iEType'] == 'Science')]))
            else:
                self.design_data["dBdt"].append(0)

        for i, field in enumerate(self.data['dField']):
            """To determine the number of apogee a dithers per design (cNAPA),
            as well as b dithers (cNAPB), and the same for NSE dithers."""
            # APOGEE dithers
            if self.design_data["dNAPA"][i] == self.design_data["dNAPB"][i]:
                if self.design_data["dNAPA"][i] != 0:
                    self.design_data['dAPSummary'].append(
                        '{}xAB'.format(self.design_data["dNAPA"][i]))
                else:
                    self.design_data['dAPSummary'].append('No APOGEE')
            else:
                self.design_data['dAPSummary'].append(
                    '{}xA {}xB'.format(self.design_data["dNAPA"][i],
                                       self.design_data["dNAPB"][i]))
            if self.design_data["dNB"][i] != 0:
                self.design_data["dBSummary"].append(
                    '{}x{}s'.format(self.design_data["dNB"][i],
                                    self.design_data["dBdt"][i]))
            else:
                self.design_data['dBSummary'].append('No BOSS')

    def hartmann_parse(self, time):
        output = '{}\n'.format(time.isot[:19])
        inputs = []
        for key in ["r1PistonMove_steps", "b1RingMove", "sp1AverageMove_steps",
                    "sp1Residuals_deg", "sp1Temp_median"]:
            time_delta =(self.support["harts"]['t' + key] - time).sec
            x = self.support["harts"][key][(time_delta < 120)
                                           & (time_delta > 0)]
            if len(x) == 0:
                inputs.append(np.nan)
            else:
                inputs.append(x[-1])
        output += f"r1 Steps: {inputs[0]:>5.0f}, b1 Ring: {inputs[1]:>4.1f}\n"
        output += f"Average Move:{inputs[2]:>5.0f}, Residuals:"
        output += f" {inputs[3]:>4.1f}, Temp: {inputs[4]:>4.1f}\n"
        return output

    def p_summary(self):
        print('=' * 80)
        print('{:^80}'.format('Observing Summary'))
        print('=' * 80)
        print(f"{'Time':>8} {'Field':>6} {'Cadence':<24}"
              f" {'APOGEE':<9} {'BOSS':<7} {'Completion':<10}")
        for i, field in enumerate(self.data['dField']):
            try:
                line = (f"{self.data['dTimes'][i][0].isot[11:19]:>8}"
                        f" {field:>6} {'':>24}"
                        f" {self.design_data['dAPSummary'][i]:<9}"
                        f" {self.design_data['dBSummary'][i]:<7}")
                print(line)
            except (IndexError, TypeError) as e:
                continue
        print()
        if len(self.ap_data["fRatio"]) > 0:
            flux_ratio = np.nanmean(np.array(self.ap_data["fRatio"]), axis=0)
            avg = np.nanmean(flux_ratio)
            missing = flux_ratio < 0.2
            faint = (flux_ratio < 0.7) & (0.2 <= flux_ratio)
            bright = ~missing & ~faint
            i_missing = np.where(missing)[0].astype(int) + 1
            i_faint = np.where(faint)[0].astype(int) + 1
            i_bright = np.where(bright)[0]
            if self.ap_image is not None:
                missing_bundles = self.ap_image.create_bundles(i_missing)
                faint_bundles = self.ap_image.create_bundles(i_faint)
                print("APOGEE Dome Flats\n"
                      f"Missing Fibers: {missing_bundles}\n"
                      f"Faint fibers: {faint_bundles}\n"
                      f"Average Throughput: {avg:.3f}")
                print()
            else:
                print("No APOGEE Dome Flats")

        print('### Notes:\n')
        start_time = Time(self.args.sjd, format="mjd")
        end_time = Time(self.args.sjd + 1, format="mjd")
        dust_sum = get_dust.get_dust(start_time, end_time, self.args.verbose)
        print('- Integrated Dust Counts: ~{:5.0f} dust-hrs'.format(
            dust_sum - dust_sum % 100))
        print('\n')

        # print('=' * 80)
        # print('{:^80}'.format('Comments Timeline'))
        # print('=' * 80)
        # print()

    @staticmethod
    def get_window(data, i, design):
        try:
            window = ((data['iTime']
                       >= data['dTime'][i])
                      & (data['iTime']
                         < data['dTime'][i + 1])
                      & (data["iDesign"][i] == design)
                      )

        except IndexError:
            try:
                window = ((data['iTime'] >= data['dTime'][i])
                          & (data['iTime'] < Time.now() + 0.3)
                          & (data["iDesign"][i] == design)
                          )
            except IndexError:
                window = np.array([False] * len(data['iTime']))

        return window

    def p_data(self):
        start = Time(self.args.sjd - 0.3, format='mjd')
        end = Time(self.args.sjd + 1, format='mjd') - 0.3
        end = Time.now() if Time.now() < end else end
        tel = log_support.LogSupport(start, end, self.args)
        tel.get_hartmann(self.support)

        print('=' * 80)
        print('{:^80}'.format('Data Log'))
        print('=' * 80 + '\n')
        for i, field in enumerate(self.data['dField']):
            print('### Field {}\n'.format(field))
            if field in self.ap_data['dField']:
                ap_design = np.where(field == self.ap_data['dField'])[0][0]

                print('# APOGEE')
                print('{:<5} {:<8} {:>}-{:<6} {:<8} {:<12} {:<4} {:<6} {:<5}'
                      ' {:<4}'.format('MJD', 'UTC', "Design", "Config",
                                      'Exposure', 'Type',
                                      'Dith', 'Reads', 'Arch',
                                      'Seeing'))
                print('-' * 80)
                # window = self.get_window(self.ap_data, ap_design, design)
                window = self.ap_data["iField"] == field
                for (mjd, iso, des, conf, exp_id, exp_type, dith, nread,
                     detectors, see) in zip(
                    self.ap_data['iTime'][window].mjd + 0.3,
                    self.ap_data['iTime'][window].iso,
                    self.ap_data["iDesign"][window],
                    self.ap_data["iConfig"][window],
                    self.ap_data['iID'][window],
                    self.ap_data['iEType'][window],
                    self.ap_data['iDither'][window],
                    self.ap_data['iNRead'][window],
                    self.ap_data['iDetector'][window],
                    self.ap_data['iSeeing'][window]
                ):
                    print('{:<5.0f} {:0>8} {:>6.0f}-{:<6.0f} {:<8.0f} {:<12}'
                          ' {:<4} {:>5} {:<5}'
                          ' {:>4.1f}'.format(int(mjd), iso[11:19], des, conf,
                                             exp_id, exp_type,
                                             dith, nread, detectors, see))
                print()
                if field in self.ap_data['dField']:
                    for j, dome in enumerate(self.ap_data['fField']):
                        if dome == field:
                            print(self.ap_data['fTime'][j].iso)
                            print(textwrap.fill('Missing fibers: {}'.format(
                                self.ap_data['fMissing'][j]), 80))
                            print(textwrap.fill('Faint fibers: {}'.format(
                                self.ap_data['fFaint'][j]), 80))
                            print(f"Average Throughput:"
                                  f" {np.nanmean(self.ap_data['fRatio'][j]):.2f}")
                            print()

            if field in self.b_data['dField']:
                print('# BOSS')
                print('{:<5} {:<8} {:>6}-{:<6} {:<8} {:<7} {:<5} {:<5} {:<5}'
                      ''.format('MJD', 'UTC', "Design", "Config", 'Exposure',
                                'Type', 'SOS', 'ETime', 'Hart'))
                print('-' * 80)
                # i is an index for data, but it will disagree with b_data
                # if there is an apogee-onlydesign
                b_field = np.where(field == self.b_data['dField'])[0][0]
                # window = self.get_window(self.b_data, b_design, design)
                window = self.b_data["iField"] == field
                for (mjd, iso, design, conf, exp_id, exp_type,
                     detectors, etime, hart) in zip(
                    self.b_data['iTime'][window].mjd + 0.3,
                    self.b_data['iTime'][window].iso,
                    self.b_data["iDesign"][window],
                    self.b_data["iConfig"][window],
                    self.b_data['iID'][window],
                    self.b_data['iEType'][window],
                    self.b_data['iDetector'][window],
                    self.b_data['idt'][window],
                    self.b_data['iHart'][window],
                ):
                    try:
                        print('{:<5.0f} {:0>8} {:>6.0f}-{:<6.0f} {:0>8.0f} {:<7}'
                          ' {:<5}'
                          ' {:>5.0f} {:<5}'
                          ''.format(int(mjd), iso[11:19], design, conf, exp_id,
                                    exp_type.strip(), detectors, etime,
                                    hart))
                    except Exception as e:
                        print(int(mjd), iso[11:19])
                hwindow = self.b_data["hField"] == field
                for t in self.b_data["hTime"][hwindow]:
                    print(self.hartmann_parse(t))
                print()

    def p_boss(self):
        print('=' * 80)
        print('{:^80}'.format('BOSS Data Summary'))
        print('=' * 80 + '\n')
        print('{:<5} {:<8} {:<20} {:<8} {:<7} {:<5} {:<5} {:<5}'
              ''.format('MJD', 'UTC', 'Field-Design-Config', 'Exposure', 'Type',
                        'SOS', 'ETime', 'Hart'))
        print('-' * 80)
        for (mjd, iso, field, design, config, exp_id, exp_type, 
             detectors, etime,
             hart) in zip(self.b_data['iTime'].mjd + 0.3,
                          self.b_data['iTime'].iso,
                          self.b_data['iField'],
                          self.b_data["iDesign"],
                          self.b_data['iConfig'],
                          self.b_data['iID'],
                          self.b_data['iEType'],
                          self.b_data['iDetector'],
                          self.b_data['idt'],
                          self.b_data['iHart']):
            try:
                print('{:<5.0f} {:>8} {:>6.0f}-{:>6}-{:<6.0f} {:0>8.0f} {:<7}'
                  ' {:<5}'
                  ' {:>5.0f} {:<5}'
                  ''.format(int(mjd), iso[11:19], field, design, config, exp_id,
                            exp_type.strip(), detectors, etime, hart))
            except TypeError:
                 continue
        print()

    def p_apogee(self):
        print('=' * 80)
        print('{:^80}'.format('APOGEE Data Summary'))
        print('=' * 80 + '\n')
        print('{:<5} {:<8} {:<20} {:<8} {:<12} {:<4} {:<5} {:<5}'
              ''.format('MJD', 'UTC', ' Field-Design-Config', 'Exposure', 'Type',
                        'Dith', 'Reads', 'Arch'))
        print('-' * 80)
        if self.args.morning:
            for (mjd, iso, field, design, config, exp_id, exp_type, dith, nread,
                 detectors) in zip(
                self.ap_data['iTime'].mjd[self.morning_filter] + 0.3,
                self.ap_data['iTime'].iso[self.morning_filter],
                self.ap_data["iField"][self.morning_filter],
                self.ap_data["iDesign"][self.morning_filter],
                self.ap_data["iConfig"][self.morning_filter],
                self.ap_data['iID'][self.morning_filter],
                self.ap_data['iEType'][self.morning_filter],
                self.ap_data['iDither'][self.morning_filter],
                self.ap_data['iNRead'][self.morning_filter],
                self.ap_data['iDetector'][self.morning_filter],
            ):
                print('{:<5.0f} {:>8} {:>6.0f}-{:>6.0f}-{:<6.0f} {:<8.0f} {:<12} {:<4}'
                      ' {:>5}'
                      ' {:<5}'
                      ''.format(int(mjd), iso[11:19], field, design, config,
                                exp_id, exp_type,
                                dith, nread, detectors))

        else:
            for (mjd, iso, field, design, config, exp_id, exp_type, dith, nread,
                 detectors) in zip(
                self.ap_data['iTime'].mjd,
                self.ap_data['iTime'].iso,
                self.ap_data["iField"],
                self.ap_data["iDesign"],
                self.ap_data["iConfig"],
                self.ap_data['iID'], self.ap_data['iEType'],
                self.ap_data['iDither'], self.ap_data['iNRead'],
                self.ap_data['iDetector'],
            ):
                # print('{:<5.0f} {:>8} {:>2.0f}-{:<5.0f} {:<8.0f} {:<12} {:<4}'
                #       ' {:>6}'
                #       ' {:<8}'
                #       ' {:>6.1f}'.format(int(mjd), iso[11:19], design, plate,
                #                          exp_id, exp_type,
                #                          dith, nread, detectors, see))
                print('{:<5.0f} {:>8} {:>6.0f}-{:>6.0f}-{:<6.0f} {:<8.0f} {:<12} {:<4}'
                      ' {:>5}'
                      ' {:<5}'
                      ''.format(int(mjd), iso[11:19], field, design, config,
                                exp_id, exp_type,
                                dith, nread, detectors))

        # Usually, there are 4 ThAr and 4 UNe arcs in a night, and they're
        # assumed to be alternating ThAr UNe ThAr UNe. When you grab every
        # other, you'll have only one type, that's the first slicing, and the
        # second slicing is that you only care about the diffs between two
        # dithers taken back to back.
        wrapper = textwrap.TextWrapper(80)
        thar_str = 'ThAr Offsets: {}'.format(
            ['{:.2f}'.format(f) for f in np.diff(
                self.ap_data['aOffset'][self.ap_data['aLamp'] == 'ThAr'])])
        print('\n'.join(wrapper.wrap(thar_str)))
        une_str = 'UNe Offsets: {}'.format(
            ['{:.2f}'.format(f) for f in np.diff(
                self.ap_data['aOffset'][self.ap_data['aLamp'] == 'UNe'])])
        print('\n'.join(wrapper.wrap(une_str)))
        if len(self.ap_data['oOffset']) > 1:
            # Put it under an if in case we didn't open.
            did_move = self.ap_data["oDither"][:-
                                               1] != self.ap_data["oDither"][1:]
            rel_offsets = np.abs(self.ap_data['oOffset'][1:][did_move]
                                 - self.ap_data["oOffset"][:-1][did_move])
            obj_str = ('Object Offsets: Max: {:.2f}, Min: {:.2f}, Mean: {:.2f}'
                       ''.format(np.nanmax(rel_offsets), np.nanmin(rel_offsets),
                                 np.nanmean(rel_offsets)))
            # ['{:>6.3f}'.format(f) for f in np.diff(
            #     self.ap_data['oOffset'])])
            print('\n'.join(wrapper.wrap(obj_str)))
        # obj_offsets = []
        # prev_dither = None
        # prev_f = 0.
        # for d, f in zip(self.ap_data['oDither'], self.ap_data['oOffset']):
        #     if d != prev_dither:
        #         obj_offsets.append('{:.3f}'.format(f - prev_f))
        #     prev_dither = d
        #     prev_f = f
        # obj_str = 'Object Offsets: {}'.format(obj_offsets)
        print('\n')

    def log_support(self):
        print('=' * 80)
        print(f"{'Log Support':^80}")
        print('=' * 80)
        start = Time(self.args.sjd - 0.3, format='mjd')
        end = Time(self.args.sjd + 0.7, format='mjd')
        end = Time.now() if Time.now() < end else end
        sup = log_support.LogSupport(start, end, self.args)
        sup.set_callbacks()
        offsets = multiprocessing.Process(target=sup.get_offsets,
                                          args=(self.support,))
        focus = multiprocessing.Process(target=sup.get_focus,
                                        args=(self.support,))
        weather = multiprocessing.Process(target=sup.get_weather,
                                          args=(self.support,))
        if "harts" not in self.support.keys():
            hartmann = multiprocessing.Process(target=sup.get_hartmann,
                                               args=(self.support,))
            hartmann.start()
        offsets.start()
        focus.start()
        weather.start()
        # If these queries are timing out, you have an issue in Influx
        offsets.join()
        focus.join()
        weather.join()
        if "harts" not in self.support.keys():
            hartmann.join()
        print(self.support["offsets"])
        print(self.support["focus"])
        print(self.support["weather"])
        print(self.support["hartmann"])

    @staticmethod
    def mirror_numbers():
        print('=' * 80)
        print('{:^80}'.format('Mirror Numbers'))
        print('=' * 80 + '\n')
        try:
            mirror_nums = m4l.mirrors()
            print(mirror_nums)
        except (ConnectionRefusedError, TimeoutError) as me:
            print('Could not fetch mirror numbers:\n{}'.format(me))

    @staticmethod
    def tel_status():
        print('=' * 80)
        print('{:^80}'.format('Telescope Status'))
        print('=' * 80 + '\n')
        try:
            status = telescope_status.query()
            print(status)
        except OSError as oe:
            print(f"Couldn't get telescope status:\n{oe}")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--today', action='store_true', default=True,
                        help="Whether or not you want to search for today's"
                             " data, whether or not the night is complete."
                             " Note: must be run after 18:00Z to get the"
                             " correct sjd")
    parser.add_argument('-m', '--mjd', type=int,
                        help='If not today (-t), the mjd to search (actually'
                             ' sjd)')
    parser.add_argument('--mirrors', '--mirror', action='store_true',
                        help='Print mirror numbers using m4l.py')
    parser.add_argument("-s", '--summary', help='Print the data summary',
                        action='store_true')
    parser.add_argument('-d', '--data', action='store_true',
                        help='Print the data log')
    parser.add_argument('-p', '--print', action='store_true',
                        help='Print all possible outputs')
    parser.add_argument('-b', '--boss', action='store_true',
                        help='Print BOSS Summary')
    parser.add_argument('-a', '--apogee', action='store_true',
                        help='Print APOGEE Summary')
    parser.add_argument('-l', '--log-support', action='store_true',
                        help='Print 4 log support sections')
    parser.add_argument('-n', '--noprogress', action='store_true',
                        help='Show no progress in processing images. WARNING:'
                             ' Might be slower, but it could go either way.')
    parser.add_argument("-t", '--telstatus', action='store_true',
                        help='Print telescope status')
    parser.add_argument('--morning', action='store_true',
                        help='Only output apogee morning cals')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Increased printing for debugging')
    parser.add_argument('--legacy-aptest', action='store_true',
                        help='Use utr_cdr images for aptest instead of'
                             ' quickred for the ap_test')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    if args.mjd:
        args.sjd = args.mjd
    elif args.today:
        args.sjd = sjd.sjd()
    else:
        raise argparse.ArgumentError(args.sjd,
                                     'Must provide -t or -m in arguments')
    if args.verbose:
        print(args.sjd)
    ap_data_dir = ap_dir / '{}'.format(args.sjd)
    b_data_dir = b_dir / '{}'.format(args.sjd)
    ap_images = Path(ap_data_dir).glob('apR-a*.apz')
    try:
        for img in ap_images:
            img.exists()
    except OSError:
        pass
    ap_images = Path(ap_data_dir).glob('apR-a*.apz')

    b_images = Path(b_data_dir).glob('sdR-r1*fit.gz')
    try:
        for img in b_images:
            img.exists()
    except OSError:
        pass
    b_images = Path(b_data_dir).glob('sdR-r1*fit.gz')

    if not args.noprogress:
        try:
            ap_images = list(ap_images)
            b_images = list(b_images)
        except OSError:  # Stale NFS handle
            ap_images = list(ap_images)
            b_images = list(b_images)
    p_boss = args.boss
    p_apogee = args.apogee

    if args.print:
        args.summary = True
        args.data = True
        args.boss = True
        args.apogee = True
        p_boss = True
        p_apogee = True
        args.log_support = True  # Because this usually produces wrong results
        # args.mirrors = True
        args.telstatus = True

    if args.summary:
        args.boss = True
        args.apogee = True

    if args.morning:
        args.apogee = True
        p_apogee = True

    if args.data:
        args.boss = True
        args.apogee = True

    log = Logging(ap_images, b_images, args)
    log.parse_images()
    log.sort()
    log.count_dithers()

    if args.summary:
        log.p_summary()

    if args.data:
        log.p_data()

    if p_apogee:
        log.p_apogee()

    if p_boss:
        log.p_boss()

    if args.log_support:
        log.log_support()

    if args.mirrors:
        # pass
        log.mirror_numbers()

    if args.telstatus:
        log.tel_status()
    return log


if __name__ == '__main__':
    main()
