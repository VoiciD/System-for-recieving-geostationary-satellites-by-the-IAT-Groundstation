#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.9.2

from PyQt5 import Qt
from gnuradio import qtgui
from PyQt5 import QtCore
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import osmosdr
import time
import sip



class SDR_Software(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "SDR_Software")

        try:
            geometry = self.settings.value("geometry")
            if geometry:
                self.restoreGeometry(geometry)
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.volume = volume = 0.5
        self.ssb = ssb = 0
        self.samp_rate = samp_rate = 1e6
        self.rf_gain = rf_gain = 0
        self.demod = demod = 0
        self.channel_frequency = channel_frequency = 39.9976e6
        self.center_frequency = center_frequency = 40e6
        self.bandwidth = bandwidth = 125e3

        ##################################################
        # Blocks
        ##################################################

        self._volume_range = qtgui.Range(0, 1, 0.1, 0.5, 200)
        self._volume_win = qtgui.RangeWidget(self._volume_range, self.set_volume, "Volume", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._volume_win)
        # Create the options list
        self._ssb_options = [0, 1]
        # Create the labels list
        self._ssb_labels = ['USB', 'LSB']
        # Create the combo box
        self._ssb_tool_bar = Qt.QToolBar(self)
        self._ssb_tool_bar.addWidget(Qt.QLabel("SSB Chooser" + ": "))
        self._ssb_combo_box = Qt.QComboBox()
        self._ssb_tool_bar.addWidget(self._ssb_combo_box)
        for _label in self._ssb_labels: self._ssb_combo_box.addItem(_label)
        self._ssb_callback = lambda i: Qt.QMetaObject.invokeMethod(self._ssb_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._ssb_options.index(i)))
        self._ssb_callback(self.ssb)
        self._ssb_combo_box.currentIndexChanged.connect(
            lambda i: self.set_ssb(self._ssb_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._ssb_tool_bar)
        self._rf_gain_range = qtgui.Range(0, 30, 1, 0, 200)
        self._rf_gain_win = qtgui.RangeWidget(self._rf_gain_range, self.set_rf_gain, "RF Gain", "counter_slider", int, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._rf_gain_win)
        # Create the options list
        self._demod_options = [0, 1, 2, 3, 4]
        # Create the labels list
        self._demod_labels = ['FM', 'SSB', 'CW', 'Test SSB', 'Test SSB Filter Method']
        # Create the combo box
        self._demod_tool_bar = Qt.QToolBar(self)
        self._demod_tool_bar.addWidget(Qt.QLabel("Demodulation" + ": "))
        self._demod_combo_box = Qt.QComboBox()
        self._demod_tool_bar.addWidget(self._demod_combo_box)
        for _label in self._demod_labels: self._demod_combo_box.addItem(_label)
        self._demod_callback = lambda i: Qt.QMetaObject.invokeMethod(self._demod_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._demod_options.index(i)))
        self._demod_callback(self.demod)
        self._demod_combo_box.currentIndexChanged.connect(
            lambda i: self.set_demod(self._demod_options[i]))
        # Create the radio buttons
        self.top_layout.addWidget(self._demod_tool_bar)
        self._channel_frequency_range = qtgui.Range(30e6, 120e6, 1, 39.9976e6, 200)
        self._channel_frequency_win = qtgui.RangeWidget(self._channel_frequency_range, self.set_channel_frequency, "Channel Frequency", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._channel_frequency_win)
        self._center_frequency_range = qtgui.Range(30e6, 120e6, 1, 40e6, 200)
        self._center_frequency_win = qtgui.RangeWidget(self._center_frequency_range, self.set_center_frequency, "Center Frequency", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._center_frequency_win)
        self._bandwidth_range = qtgui.Range(1, 200e3, 1, 125e3, 200)
        self._bandwidth_win = qtgui.RangeWidget(self._bandwidth_range, self.set_bandwidth, "Filter Bandwidth", "eng_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._bandwidth_win)
        self.rational_resampler_xxx_1 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=250,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_0_0 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=250,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=250,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0 = filter.rational_resampler_fff(
                interpolation=12,
                decimation=250,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=12,
                decimation=5,
                taps=[],
                fractional_bw=0)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_frequency, #fc
            samp_rate, #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(False)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-140, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.qwidget(), Qt.QWidget)

        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 0, 0, 2, 1)
        for r in range(0, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_f(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            0, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.10)
        self.qtgui_freq_sink_x_1.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_1.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(False)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)


        self.qtgui_freq_sink_x_1.set_plot_pos_half(not False)

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_freq_sink_x_1_win)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_frequency, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis((-140), 10)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(False)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(True)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_sample_rate(samp_rate)
        self.osmosdr_source_0.set_center_freq(center_frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(0, 0)
        self.osmosdr_source_0.set_bb_gain(0, 0)
        self.osmosdr_source_0.set_antenna('QO-100', 0)
        self.osmosdr_source_0.set_bandwidth(samp_rate, 0)
        self.low_pass_filter_2_0 = filter.fir_filter_ccf(
            1,
            firdes.low_pass(
                1,
                1e6,
                bandwidth,
                500,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1_0 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                bandwidth,
                500,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_1 = filter.fir_filter_fff(
            1,
            firdes.low_pass(
                1,
                samp_rate,
                bandwidth,
                500,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_ccf(
            5,
            firdes.low_pass(
                1,
                samp_rate,
                bandwidth,
                25e3,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(1, [22], 0, samp_rate)
        self.freq_xlating_fir_filter_xxx_0 = filter.freq_xlating_fir_filter_ccc(1, [22], 0, samp_rate)
        self.blocks_swapiq_0_0 = blocks.swap_iq(1, gr.sizeof_gr_complex)
        self.blocks_swapiq_0 = blocks.swap_iq(1, gr.sizeof_gr_complex)
        self.blocks_sub_xx_0 = blocks.sub_ff(1)
        self.blocks_selector_2 = blocks.selector(gr.sizeof_float*1,demod,0)
        self.blocks_selector_2.set_enabled(True)
        self.blocks_selector_1_0_0 = blocks.selector(gr.sizeof_gr_complex*1,ssb,0)
        self.blocks_selector_1_0_0.set_enabled(True)
        self.blocks_selector_1_0 = blocks.selector(gr.sizeof_gr_complex*1,ssb,0)
        self.blocks_selector_1_0.set_enabled(True)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_float*1,ssb,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,demod)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_multiply_xx_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_1_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(volume)
        self.blocks_complex_to_real_1_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_1_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_1 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_imag_0 = blocks.complex_to_imag(1)
        self.blocks_add_xx_0 = blocks.add_vff(1)
        self.band_pass_filter_1 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                48e3,
                750,
                1250,
                500,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0_0_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                48e3,
                200,
                10e3,
                500,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_ccc(
            1,
            firdes.complex_band_pass(
                1,
                48e3,
                200,
                10e3,
                500,
                window.WIN_HAMMING,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                1e6,
                200,
                bandwidth,
                500,
                window.WIN_HAMMING,
                6.76))
        self.audio_sink_0 = audio.sink(48000, '', True)
        self.analog_sig_source_x_1_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, channel_frequency, 2, 0, 0)
        self.analog_sig_source_x_1_0 = analog.sig_source_f(samp_rate, analog.GR_SIN_WAVE, channel_frequency, 1, 0, 0)
        self.analog_sig_source_x_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, channel_frequency, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, (center_frequency-channel_frequency), 1, 0, 0)
        self.analog_fm_demod_cf_0 = analog.fm_demod_cf(
        	channel_rate=480e3,
        	audio_decim=10,
        	deviation=75000,
        	audio_pass=15000,
        	audio_stop=16000,
        	gain=1.0,
        	tau=(75e-6),
        )
        self.analog_agc2_xx_1_0_0 = analog.agc2_cc((1e-3), (1e-3), 1, 0.1, 65536)
        self.analog_agc2_xx_1_0 = analog.agc2_cc((1e-3), (1e-3), 0.1, 0.1, 65536)
        self.analog_agc2_xx_1 = analog.agc2_ff((1e-3), (1e-3), 0.1, 0.1, 65536)
        self.analog_agc2_xx_0 = analog.agc2_cc((1e-3), (1e-3), 0.1, 0.1, 65536)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_complex_to_real_1, 0))
        self.connect((self.analog_agc2_xx_1, 0), (self.band_pass_filter_0, 0))
        self.connect((self.analog_agc2_xx_1_0, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.analog_agc2_xx_1_0_0, 0), (self.band_pass_filter_0_0_0, 0))
        self.connect((self.analog_fm_demod_cf_0, 0), (self.blocks_selector_2, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.analog_sig_source_x_1_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.analog_sig_source_x_1_0_0, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_selector_2, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_complex_to_real_1_0, 0))
        self.connect((self.band_pass_filter_0_0_0, 0), (self.blocks_complex_to_real_1_0_0, 0))
        self.connect((self.band_pass_filter_1, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.blocks_complex_to_imag_0, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_complex_to_real_1, 0), (self.blocks_selector_2, 2))
        self.connect((self.blocks_complex_to_real_1_0, 0), (self.blocks_selector_2, 3))
        self.connect((self.blocks_complex_to_real_1_0_0, 0), (self.blocks_selector_2, 4))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.low_pass_filter_1, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.low_pass_filter_1_0, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.low_pass_filter_2_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_complex_to_imag_0, 0))
        self.connect((self.blocks_selector_0, 1), (self.blocks_complex_to_real_0, 0))
        self.connect((self.blocks_selector_0, 4), (self.blocks_multiply_xx_2, 0))
        self.connect((self.blocks_selector_0, 2), (self.freq_xlating_fir_filter_xxx_0, 0))
        self.connect((self.blocks_selector_0, 3), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.blocks_selector_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.rational_resampler_xxx_0_0, 0))
        self.connect((self.blocks_selector_1_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.blocks_selector_1_0_0, 0), (self.rational_resampler_xxx_0_0_0_0, 0))
        self.connect((self.blocks_selector_2, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_selector_2, 0), (self.qtgui_freq_sink_x_1, 0))
        self.connect((self.blocks_sub_xx_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.blocks_swapiq_0, 0), (self.blocks_selector_1_0, 1))
        self.connect((self.blocks_swapiq_0_0, 0), (self.blocks_selector_1_0_0, 1))
        self.connect((self.freq_xlating_fir_filter_xxx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_selector_1_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_swapiq_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.low_pass_filter_1, 0), (self.blocks_sub_xx_0, 1))
        self.connect((self.low_pass_filter_1_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.low_pass_filter_1_0, 0), (self.blocks_sub_xx_0, 0))
        self.connect((self.low_pass_filter_2_0, 0), (self.blocks_selector_1_0_0, 0))
        self.connect((self.low_pass_filter_2_0, 0), (self.blocks_swapiq_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.analog_fm_demod_cf_0, 0))
        self.connect((self.rational_resampler_xxx_0_0, 0), (self.analog_agc2_xx_1, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.analog_agc2_xx_1_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0_0, 0), (self.analog_agc2_xx_1_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.band_pass_filter_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "SDR_Software")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_volume(self):
        return self.volume

    def set_volume(self, volume):
        self.volume = volume
        self.blocks_multiply_const_vxx_0.set_k(self.volume)

    def get_ssb(self):
        return self.ssb

    def set_ssb(self, ssb):
        self.ssb = ssb
        self._ssb_callback(self.ssb)
        self.blocks_selector_1.set_input_index(self.ssb)
        self.blocks_selector_1_0.set_input_index(self.ssb)
        self.blocks_selector_1_0_0.set_input_index(self.ssb)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1_0.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1_0_0.set_sampling_freq(self.samp_rate)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, 25e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, 500, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, 500, window.WIN_HAMMING, 6.76))
        self.osmosdr_source_0.set_sample_rate(self.samp_rate)
        self.osmosdr_source_0.set_bandwidth(self.samp_rate, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_frequency, self.samp_rate)
        self.qtgui_freq_sink_x_1.set_frequency_range(0, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_frequency, self.samp_rate)

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)

    def get_demod(self):
        return self.demod

    def set_demod(self, demod):
        self.demod = demod
        self._demod_callback(self.demod)
        self.blocks_selector_0.set_output_index(self.demod)
        self.blocks_selector_2.set_input_index(self.demod)

    def get_channel_frequency(self):
        return self.channel_frequency

    def set_channel_frequency(self, channel_frequency):
        self.channel_frequency = channel_frequency
        self.analog_sig_source_x_0.set_frequency((self.center_frequency-self.channel_frequency))
        self.analog_sig_source_x_1.set_frequency(self.channel_frequency)
        self.analog_sig_source_x_1_0.set_frequency(self.channel_frequency)
        self.analog_sig_source_x_1_0_0.set_frequency(self.channel_frequency)

    def get_center_frequency(self):
        return self.center_frequency

    def set_center_frequency(self, center_frequency):
        self.center_frequency = center_frequency
        self.analog_sig_source_x_0.set_frequency((self.center_frequency-self.channel_frequency))
        self.osmosdr_source_0.set_center_freq(self.center_frequency, 0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_frequency, self.samp_rate)
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.center_frequency, self.samp_rate)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, 1e6, 200, self.bandwidth, 500, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, 25e3, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, 500, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_1_0.set_taps(firdes.low_pass(1, self.samp_rate, self.bandwidth, 500, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_2_0.set_taps(firdes.low_pass(1, 1e6, self.bandwidth, 500, window.WIN_HAMMING, 6.76))




def main(top_block_cls=SDR_Software, options=None):

    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
