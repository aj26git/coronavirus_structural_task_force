# script auto-generated by phenix.molprobity


from __future__ import absolute_import, division, print_function
from six.moves import cPickle as pickle
from six.moves import range
try :
  import gobject
except ImportError :
  gobject = None
import sys

class coot_extension_gui(object):
  def __init__(self, title):
    import gtk
    self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    scrolled_win = gtk.ScrolledWindow()
    self.outside_vbox = gtk.VBox(False, 2)
    self.inside_vbox = gtk.VBox(False, 0)
    self.window.set_title(title)
    self.inside_vbox.set_border_width(0)
    self.window.add(self.outside_vbox)
    self.outside_vbox.pack_start(scrolled_win, True, True, 0)
    scrolled_win.add_with_viewport(self.inside_vbox)
    scrolled_win.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)

  def finish_window(self):
    import gtk
    self.outside_vbox.set_border_width(2)
    ok_button = gtk.Button("  Close  ")
    self.outside_vbox.pack_end(ok_button, False, False, 0)
    ok_button.connect("clicked", lambda b: self.destroy_window())
    self.window.connect("delete_event", lambda a, b: self.destroy_window())
    self.window.show_all()

  def destroy_window(self, *args):
    self.window.destroy()
    self.window = None

  def confirm_data(self, data):
    for data_key in self.data_keys :
      outlier_list = data.get(data_key)
      if outlier_list is not None and len(outlier_list) > 0 :
        return True
    return False

  def create_property_lists(self, data):
    import gtk
    for data_key in self.data_keys :
      outlier_list = data[data_key]
      if outlier_list is None or len(outlier_list) == 0 :
        continue
      else :
        frame = gtk.Frame(self.data_titles[data_key])
        vbox = gtk.VBox(False, 2)
        frame.set_border_width(6)
        frame.add(vbox)
        self.add_top_widgets(data_key, vbox)
        self.inside_vbox.pack_start(frame, False, False, 5)
        list_obj = residue_properties_list(
          columns=self.data_names[data_key],
          column_types=self.data_types[data_key],
          rows=outlier_list,
          box=vbox)

# Molprobity result viewer
class coot_molprobity_todo_list_gui(coot_extension_gui):
  data_keys = [ "rama", "rota", "cbeta", "probe" ]
  data_titles = { "rama"  : "Ramachandran outliers",
                  "rota"  : "Rotamer outliers",
                  "cbeta" : "C-beta outliers",
                  "probe" : "Severe clashes" }
  data_names = { "rama"  : ["Chain", "Residue", "Name", "Score"],
                 "rota"  : ["Chain", "Residue", "Name", "Score"],
                 "cbeta" : ["Chain", "Residue", "Name", "Conf.", "Deviation"],
                 "probe" : ["Atom 1", "Atom 2", "Overlap"] }
  if (gobject is not None):
    data_types = { "rama" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "rota" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                             gobject.TYPE_STRING, gobject.TYPE_FLOAT,
                             gobject.TYPE_PYOBJECT],
                   "cbeta" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT],
                   "probe" : [gobject.TYPE_STRING, gobject.TYPE_STRING,
                              gobject.TYPE_FLOAT, gobject.TYPE_PYOBJECT] }
  else :
    data_types = dict([ (s, []) for s in ["rama","rota","cbeta","probe"] ])

  def __init__(self, data_file=None, data=None):
    assert ([data, data_file].count(None) == 1)
    if (data is None):
      data = load_pkl(data_file)
    if not self.confirm_data(data):
      return
    coot_extension_gui.__init__(self, "MolProbity to-do list")
    self.dots_btn = None
    self.dots2_btn = None
    self._overlaps_only = True
    self.window.set_default_size(420, 600)
    self.create_property_lists(data)
    self.finish_window()

  def add_top_widgets(self, data_key, box):
    import gtk
    if data_key == "probe" :
      hbox = gtk.HBox(False, 2)
      self.dots_btn = gtk.CheckButton("Show Probe dots")
      hbox.pack_start(self.dots_btn, False, False, 5)
      self.dots_btn.connect("toggled", self.toggle_probe_dots)
      self.dots2_btn = gtk.CheckButton("Overlaps only")
      hbox.pack_start(self.dots2_btn, False, False, 5)
      self.dots2_btn.connect("toggled", self.toggle_all_probe_dots)
      self.dots2_btn.set_active(True)
      self.toggle_probe_dots()
      box.pack_start(hbox, False, False, 0)

  def toggle_probe_dots(self, *args):
    if self.dots_btn is not None :
      show_dots = self.dots_btn.get_active()
      overlaps_only = self.dots2_btn.get_active()
      if show_dots :
        self.dots2_btn.set_sensitive(True)
      else :
        self.dots2_btn.set_sensitive(False)
      show_probe_dots(show_dots, overlaps_only)

  def toggle_all_probe_dots(self, *args):
    if self.dots2_btn is not None :
      self._overlaps_only = self.dots2_btn.get_active()
      self.toggle_probe_dots()

class rsc_todo_list_gui(coot_extension_gui):
  data_keys = ["by_res", "by_atom"]
  data_titles = ["Real-space correlation by residue",
                 "Real-space correlation by atom"]
  data_names = {}
  data_types = {}

class residue_properties_list(object):
  def __init__(self, columns, column_types, rows, box,
      default_size=(380,200)):
    assert len(columns) == (len(column_types) - 1)
    if (len(rows) > 0) and (len(rows[0]) != len(column_types)):
      raise RuntimeError("Wrong number of rows:\n%s" % str(rows[0]))
    import gtk
    self.liststore = gtk.ListStore(*column_types)
    self.listmodel = gtk.TreeModelSort(self.liststore)
    self.listctrl = gtk.TreeView(self.listmodel)
    self.listctrl.column = [None]*len(columns)
    self.listctrl.cell = [None]*len(columns)
    for i, column_label in enumerate(columns):
      cell = gtk.CellRendererText()
      column = gtk.TreeViewColumn(column_label)
      self.listctrl.append_column(column)
      column.set_sort_column_id(i)
      column.pack_start(cell, True)
      column.set_attributes(cell, text=i)
    self.listctrl.get_selection().set_mode(gtk.SELECTION_SINGLE)
    for row in rows :
      self.listmodel.get_model().append(row)
    self.listctrl.connect("cursor-changed", self.OnChange)
    sw = gtk.ScrolledWindow()
    w, h = default_size
    if len(rows) > 10 :
      sw.set_size_request(w, h)
    else :
      sw.set_size_request(w, 30 + (20 * len(rows)))
    sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
    box.pack_start(sw, False, False, 5)
    inside_vbox = gtk.VBox(False, 0)
    sw.add(self.listctrl)

  def OnChange(self, treeview):
    import coot # import dependency
    selection = self.listctrl.get_selection()
    (model, tree_iter) = selection.get_selected()
    if tree_iter is not None :
      row = model[tree_iter]
      xyz = row[-1]
      if isinstance(xyz, tuple) and len(xyz) == 3 :
        set_rotation_centre(*xyz)
        set_zoom(30)
        graphics_draw()

def show_probe_dots(show_dots, overlaps_only):
  import coot # import dependency
  n_objects = number_of_generic_objects()
  sys.stdout.flush()
  if show_dots :
    for object_number in range(n_objects):
      obj_name = generic_object_name(object_number)
      if overlaps_only and not obj_name in ["small overlap", "bad overlap"] :
        sys.stdout.flush()
        set_display_generic_object(object_number, 0)
      else :
        set_display_generic_object(object_number, 1)
  else :
    sys.stdout.flush()
    for object_number in range(n_objects):
      set_display_generic_object(object_number, 0)

def load_pkl(file_name):
  pkl = open(file_name, "rb")
  data = pickle.load(pkl)
  pkl.close()
  return data

data = {}
data['rama'] = []
data['omega'] = []
data['rota'] = [('A', ' 101 ', 'ILE', 0.24570492735262925, (320.361, 237.36699999999993, 255.14300000000003)), ('A', ' 120 ', 'VAL', 0.189583485180365, (319.367, 243.56499999999997, 248.304)), ('A', ' 212 ', 'LEU', 0.12499983228207392, (322.771, 235.94600000000003, 273.79)), ('A', ' 387 ', 'LEU', 0.18516551027206893, (264.281, 250.14199999999994, 237.63)), ('A', ' 581 ', 'THR', 0.10383640768841695, (251.38000000000014, 237.08899999999994, 262.65700000000004)), ('A', ' 914 ', 'ASN', 0.2987064457459408, (291.272, 268.64399999999995, 344.219)), ('B', ' 125 ', 'ASN', 0.05192449894329314, (227.1300000000001, 247.77399999999997, 247.53100000000003)), ('B', ' 130 ', 'VAL', 0.28028497966475785, (236.35900000000012, 259.396, 241.518)), ('B', ' 136 ', 'CYS', 0.29157213301767815, (222.59100000000015, 268.02, 238.349)), ('B', ' 141 ', 'LEU', 0.23428092419399538, (217.73500000000013, 259.024, 245.486)), ('B', ' 212 ', 'LEU', 0.24093427120688427, (217.2950000000001, 260.327, 271.998)), ('B', ' 281 ', 'GLU', 0.29801544650580225, (245.4280000000001, 250.963, 281.021)), ('B', ' 328 ', 'ARG', 0.01764220598358408, (254.65900000000005, 309.692, 257.909)), ('B', ' 362 ', 'VAL', 0.08839911003922943, (259.56999999999994, 316.216, 246.99200000000002)), ('B', ' 441 ', 'LEU', 0.25254742074880376, (250.52500000000003, 329.111, 219.139)), ('C', ' 141 ', 'LEU', 0.2516580419760369, (291.5129999999999, 337.9019999999999, 248.54600000000002)), ('C', ' 212 ', 'LEU', 0.20336719970811898, (292.6939999999999, 337.75099999999986, 275.683)), ('C', ' 234 ', 'ASN', 0.287597964294551, (287.93299999999994, 312.625, 247.36000000000004)), ('C', ' 382 ', 'VAL', 0.20870912389917953, (294.464, 277.126, 249.87800000000001)), ('C', ' 553 ', 'THR', 0.1336779190146792, (317.536, 281.746, 272.9700000000001)), ('C', ' 864 ', 'LEU', 0.09363100537240503, (254.19899999999996, 289.34, 299.7300000000001)), ('C', ' 866 ', 'THR', 0.173376036830131, (255.044, 294.541, 303.403)), ('C', ' 896 ', 'ILE', 0.20419589950171785, (258.6849999999999, 289.476, 335.162)), ('C', ' 985 ', 'ASP', 0.1172552415931247, (264.081, 285.929, 252.46500000000006))]
data['cbeta'] = []
data['probe'] = [(' C  97  LYS  HB3', ' C 186  PHE  HA ', -0.725, (290.056, 340.263, 266.679)), (' B  99  ASN HD22', ' B 178  ASP  H  ', -0.69, (219.536, 251.535, 255.88)), (' C 422  ASN HD21', ' C 454  ARG  H  ', -0.648, (286.474, 256.601, 233.159)), (' A 103  GLY  HA3', ' A 120  VAL  HA ', -0.611, (318.402, 242.579, 249.263)), (' A  97  LYS  HB3', ' A 186  PHE  HA ', -0.583, (325.477, 236.035, 266.094)), (' B  21  ARG  NH2', ' B  79  PHE  O  ', -0.581, (215.214, 270.739, 248.983)), (' C 186  PHE  HE2', ' C 214  ARG  HB3', -0.578, (295.826, 337.043, 268.051)), (' C1047  TYR  HB2', ' C1067  TYR  HB3', -0.578, (279.746, 290.649, 329.131)), (' B 193  VAL  HB ', ' B 204  TYR  HB2', -0.572, (236.227, 261.244, 260.709)), (' B  97  LYS  HB3', ' B 186  PHE  HA ', -0.566, (215.823, 257.411, 264.669)), (' B 985  ASP  N  ', ' B 985  ASP  OD1', -0.566, (274.659, 262.344, 251.718)), (' B 396  TYR  HB2', ' B 514  SER  HB3', -0.566, (266.788, 314.472, 232.928)), (' B 592  PHE  H  ', ' B 634  ARG HH22', -0.558, (250.983, 296.484, 278.929)), (' C 985  ASP  N  ', ' C 985  ASP  OD2', -0.557, (265.453, 286.257, 251.443)), (' A1090  PRO  O  ', ' B 913  GLN  NE2', -0.553, (270.171, 266.167, 344.579)), (' A1028  LYS  NZ ', ' A1042  PHE  O  ', -0.544, (284.933, 271.211, 316.424)), (' B 126  VAL  HB ', ' B 172  SER  HB3', -0.538, (231.761, 249.304, 249.375)), (' B 822  LEU HD21', ' B 938  LEU HD13', -0.537, (256.326, 259.642, 311.516)), (' A 558  LYS  HA ', ' A 584  ILE HG13', -0.533, (248.443, 242.641, 272.373)), (' C 145  TYR  HB3', ' C 247  SER  HA ', -0.531, (291.083, 351.07, 251.758)), (' B 598  ILE  HB ', ' B 609  ALA  HB3', -0.53, (241.809, 284.011, 290.504)), (' B 985  ASP  HB2', ' B 987  PRO  HD2', -0.53, (278.19, 261.429, 251.334)), (' B 103  GLY  HA3', ' B 120  VAL  HA ', -0.529, (227.141, 258.147, 248.576)), (' A 985  ASP  N  ', ' A 985  ASP  OD1', -0.526, (292.292, 283.262, 252.63)), (' B 433  VAL HG22', ' B 512  VAL HG12', -0.524, (260.031, 311.915, 226.287)), (' B1006  THR HG22', ' B1010  GLN HE21', -0.522, (269.644, 272.511, 283.241)), (' C  34  ARG  HE ', ' C 217  PRO  HG2', -0.518, (289.846, 327.442, 272.793)), (' C 985  ASP  HB2', ' C 987  PRO  HD2', -0.517, (262.891, 283.292, 251.659)), (' A  52  GLN  NE2', ' A 274  THR  OG1', -0.515, (295.408, 252.82, 270.016)), (' B 576  VAL  HB ', ' B 587  ILE HD11', -0.514, (260.615, 307.49, 269.406)), (' A 455  LEU HD22', ' A 493  GLN HE22', -0.51, (253.121, 255.023, 201.814)), (' A 985  ASP  HB2', ' A 987  PRO  HD2', -0.509, (291.06, 286.844, 252.168)), (' A 777  ASN  OD1', ' A1019  ARG  NH1', -0.508, (286.247, 284.325, 303.124)), (' C1011  GLN  OE1', ' C1014  ARG  NH1', -0.506, (272.819, 288.23, 289.621)), (' A1076  THR  HB ', ' A1097  SER  HB3', -0.506, (275.172, 249.998, 346.463)), (' C 590  CYS  O  ', ' C 634  ARG  NH2', -0.505, (307.764, 290.212, 277.621)), (' B  30  ASN HD21', ' B  59  PHE  HA ', -0.504, (228.335, 273.419, 273.989)), (' B  89  GLY  HA2', ' B 195  LYS  HG2', -0.5, (238.209, 267.206, 258.51)), (' C  66  HIS  HA ', ' C 214  ARG HH22', -0.497, (300.151, 334.107, 264.366)), (' B 454  ARG HH22', ' B 471  GLU  H  ', -0.495, (276.211, 319.525, 210.923)), (' A 106  PHE  HB2', ' A 117  LEU  HB3', -0.494, (309.27, 245.449, 247.608)), (' A  23  GLN  NE2', ' A  79  PHE  O  ', -0.492, (314.363, 224.414, 252.576)), (' C 729  VAL  H  ', ' C1059  GLY  HA2', -0.492, (269.138, 290.678, 305.382)), (' B  95  THR HG22', ' B 189  LEU HD13', -0.487, (223.678, 260.811, 265.766)), (' A1035  GLY  HA3', ' C1040  VAL HG21', -0.487, (285.564, 280.107, 325.467)), (' B1076  THR  HB ', ' B1097  SER  HB3', -0.486, (253.563, 288.792, 347.615)), (' B 143  VAL HG11', ' B 179  LEU  HB3', -0.484, (214.097, 252.503, 250.082)), (' B 742  ILE  O  ', ' B1000  ARG  NH1', -0.482, (272.775, 261.081, 270.375)), (' C 234  ASN  N  ', ' C 234  ASN  OD1', -0.482, (287.394, 312.797, 245.511)), (' B 822  LEU HD13', ' B1061  VAL HG21', -0.481, (260.14, 259.092, 309.873)), (' B 478  THR HG21', ' B 486  PHE  HD2', -0.48, (279.026, 315.845, 192.801)), (' A 274  THR  HB ', ' A 291  CYS  HB2', -0.479, (296.279, 251.311, 273.652)), (' B 499  PRO  HA ', ' B 506  GLN HE22', -0.479, (246.321, 320.782, 212.107)), (' C 730  SER  HB3', ' C1058  HIS  HA ', -0.478, (265.916, 292.272, 302.664)), (' C 343  ASN  HB2', ' C 372  ALA  HB2', -0.477, (301.315, 276.083, 228.171)), (' A 821  LEU HD21', ' A 939  SER  HB3', -0.475, (306.367, 264.345, 311.997)), (' B 498  GLN  H  ', ' B 505  TYR  HB3', -0.473, (250.492, 319.757, 209.261)), (' B 119  ILE HG12', ' B 128  ILE HG23', -0.473, (234.434, 257.322, 247.568)), (' B 253  ASP  N  ', ' B 253  ASP  OD1', -0.47, (205.206, 261.967, 241.292)), (' B1047  TYR  HB2', ' B1067  TYR  HB3', -0.469, (261.77, 272.023, 328.58)), (' A 193  VAL  HB ', ' A 204  TYR  HB2', -0.469, (310.737, 249.945, 261.292)), (' C 246  ARG  NH1', ' C 252  GLY  O  ', -0.467, (296.397, 346.376, 245.291)), (' C1091  ARG  HE ', ' C1121  PHE  HB3', -0.466, (283.092, 272.953, 350.222)), (' C 403  ARG  NH2', ' C 495  TYR  O  ', -0.465, (283.168, 263.334, 222.894)), (' A 375  SER  H  ', ' A 436  TRP  HA ', -0.464, (261.13, 238.652, 222.058)), (' B 365  TYR  H  ', ' B 527  PRO  HG3', -0.46, (254.236, 311.724, 242.373)), (' B 853  GLN  HB3', ' B 858  LEU  HB2', -0.46, (267.596, 255.992, 282.211)), (' A 918  GLU  HG2', ' C1128  VAL HG11', -0.46, (296.496, 264.937, 347.005)), (' A 278  LYS  HD3', ' A 287  ASP  HB3', -0.459, (309.143, 253.869, 280.34)), (' B  40  ASP  N  ', ' B  40  ASP  OD2', -0.459, (247.18, 259.386, 267.337)), (' C 148  ASN  N  ', ' C 148  ASN  OD1', -0.457, (285.492, 357.765, 247.639)), (' C 957  GLN  O  ', ' C 961  THR  OG1', -0.457, (274.853, 293.323, 284.145)), (' B 442  ASP  N  ', ' B 442  ASP  OD2', -0.456, (251.351, 327.156, 216.944)), (' B1106  GLN  HG3', ' B1109  PHE  H  ', -0.454, (260.234, 276.589, 340.286)), (' A 430  THR  OG1', ' A 515  PHE  O  ', -0.454, (258.811, 257.198, 232.776)), (' A 713  ALA  HB3', ' B 894  LEU  HB3', -0.453, (278.316, 253.191, 334.011)), (' C 276  LEU HD22', ' C 301  CYS  HA ', -0.453, (285.94, 306.745, 281.291)), (' C 428  ASP  N  ', ' C 428  ASP  OD1', -0.452, (288.797, 265.896, 252.195)), (' A  92  PHE  HB3', ' A 192  PHE  HB2', -0.452, (313.119, 243.749, 259.317)), (' C  84  LEU HD22', ' C 267  VAL HG11', -0.452, (297.578, 322.357, 258.773)), (' A 406  GLU  HA ', ' A 409  GLN  HG3', -0.451, (262.352, 250.524, 212.976)), (' A 319  ARG HH12', ' B 744  GLY  HA2', -0.45, (275.933, 254.54, 272.01)), (' C 895  GLN  H  ', ' C 895  GLN  HG3', -0.45, (253.539, 286.756, 334.074)), (' A 457  ARG  NH1', ' A 467  ASP  OD1', -0.45, (247.762, 260.467, 212.182)), (' B 119  ILE HG23', ' B 128  ILE HG12', -0.45, (233.049, 255.626, 248.747)), (' B 567  ARG  HD2', ' C  44  ARG HH12', -0.448, (271.568, 306.097, 272.61)), (' C 102  ARG  O  ', ' C 121  ASN  HB3', -0.448, (285.499, 333.236, 253.934)), (' A 947  LYS  HB2', ' A 947  LYS  HE2', -0.447, (293.019, 266.366, 306.197)), (' B  81  ASN  N  ', ' B  81  ASN  OD1', -0.447, (219.246, 270.757, 250.053)), (' B  34  ARG  NH2', ' B 191  GLU  OE2', -0.444, (229.262, 260.933, 268.111)), (' B 457  ARG HH21', ' B 469  SER  HB2', -0.443, (277.504, 317.932, 215.872)), (' B 410  ILE HD13', ' B 419  ALA  HB2', -0.441, (262.659, 309.534, 218.877)), (' C1106  GLN  HG3', ' C1108  ASN  H  ', -0.441, (284.31, 287.068, 340.501)), (' A  40  ASP  N  ', ' A  40  ASP  OD1', -0.438, (306.012, 260.006, 265.885)), (' A 253  ASP  N  ', ' A 253  ASP  OD2', -0.437, (328.982, 221.803, 244.892)), (' A 142  GLY  HA3', ' A 156  GLU  HB2', -0.437, (326.03, 231.549, 244.507)), (' B 394  ASN  N  ', ' B 394  ASN  OD1', -0.437, (269.33, 313.006, 240.132)), (' A 745  ASP  HB2', ' A 978  ASN HD21', -0.437, (300.18, 284.837, 266.618)), (' A 148  ASN  N  ', ' A 148  ASN  OD1', -0.436, (343.042, 230.825, 244.961)), (' C  18  LEU  HB2', ' C  21  ARG  HD2', -0.435, (303.588, 337.719, 248.004)), (' A  64  TRP  HE1', ' A 264  ALA  HB1', -0.434, (315.412, 231.987, 265.318)), (' A 983  ARG  HA ', ' C 390  LEU HD11', -0.434, (298.773, 279.514, 253.67)), (' A 559  PHE  HB2', ' A 577  ARG HH21', -0.433, (247.752, 245.595, 269.304)), (' A 318  PHE  H  ', ' A 594  GLY  HA2', -0.43, (279.477, 248.732, 279.117)), (' C 790  LYS  HA ', ' C 790  LYS  HD3', -0.43, (251.443, 295.787, 320.444)), (' C 153  MET  H  ', ' C 153  MET  HG3', -0.427, (284.464, 348.577, 248.4)), (' C 110  LEU HD22', ' C 135  PHE  HE1', -0.426, (291.951, 323.607, 244.263)), (' B  36  VAL  HB ', ' B 221  SER  HB3', -0.426, (235.077, 262.696, 270.821)), (' C  44  ARG  HB3', ' C  47  VAL HG12', -0.424, (273.2, 310.477, 277.696)), (' B 106  PHE  HB2', ' B 117  LEU  HB3', -0.423, (234.861, 264.283, 246.873)), (' B  44  ARG HH11', ' B  47  VAL HG11', -0.422, (251.506, 258.673, 275.402)), (' A 454  ARG  HD2', ' A 491  PRO  HB2', -0.422, (249.608, 257.638, 206.995)), (' A 106  PHE  HB3', ' A 235  ILE HD12', -0.422, (306.623, 245.47, 248.606)), (' B1115  ILE HG22', ' B1137  VAL HG13', -0.421, (265.377, 283.973, 356.77)), (' B  83  VAL HG12', ' B 237  ARG  HB3', -0.421, (229.547, 273.082, 247.333)), (' C 962  LEU  HA ', ' C 965  GLN HE21', -0.417, (272.206, 290.425, 279.126)), (' A  81  ASN  N  ', ' A  81  ASN  OD1', -0.417, (312.802, 228.184, 252.082)), (' C1119  ASN  HA ', ' C1119  ASN HD22', -0.417, (281.55, 279.038, 351.432)), (' B 329  PHE  N  ', ' B 330  PRO  HD2', -0.415, (255.792, 310.558, 255.599)), (' C 729  VAL HG23', ' C1022  ALA  HA ', -0.415, (268.711, 284.813, 306.609)), (' C 246  ARG  HD2', ' C 252  GLY  HA2', -0.415, (296.243, 347.36, 248.009)), (' A 246  ARG  NH1', ' A 252  GLY  O  ', -0.414, (328.733, 225.436, 243.882)), (' B 611  LEU HD13', ' B 650  LEU HD13', -0.414, (243.925, 289.177, 291.324)), (' A 182  LYS  HB2', ' A 182  LYS  HE3', -0.414, (330.056, 232.315, 263.801)), (' B  68  ILE  HA ', ' B 262  ALA  HA ', -0.413, (211.964, 264.163, 258.597)), (' B 598  ILE HD11', ' B 611  LEU HD22', -0.413, (245.722, 286.845, 291.94)), (' C 401  VAL HG22', ' C 509  ARG  HG2', -0.411, (294.682, 267.814, 227.76)), (' A 310  LYS  HB2', ' A 310  LYS  HE3', -0.41, (294.273, 250.32, 297.014)), (' B 428  ASP  N  ', ' B 428  ASP  OD2', -0.41, (268.48, 301.83, 228.892)), (' C 374  PHE  HA ', ' C 436  TRP  HB3', -0.408, (294.552, 277.276, 230.524)), (' A 153  MET  H  ', ' A 153  MET  HG3', -0.408, (335.493, 235.822, 245.85)), (' A 819  GLU  HG2', ' A1055  SER  H  ', -0.408, (301.292, 275.871, 312.988)), (' C 881  THR  O  ', ' C 901  GLN  NE2', -0.408, (262.381, 290.722, 329.818)), (' A 822  LEU HD13', ' A1061  VAL HG21', -0.406, (299.059, 270.805, 310.825)), (' A 277  LEU  HA ', ' A 277  LEU HD13', -0.404, (305.968, 255.292, 274.295)), (' A1142  GLN  HB3', ' A1143  PRO  HD3', -0.403, (275.623, 264.951, 366.065)), (' B 887  THR HG21', ' B 894  LEU HD12', -0.402, (278.885, 257.63, 331.807)), (' B 318  PHE  H  ', ' B 594  GLY  HA2', -0.402, (251.317, 288.832, 280.787)), (' C 718  PHE  HA ', ' C1069  PRO  HA ', -0.402, (284.95, 295.632, 332.691)), (' A 569  ILE  HA ', ' A 569  ILE HD12', -0.401, (254.047, 256.319, 280.462)), (' A  68  ILE HG23', ' A  70  VAL  H  ', -0.4, (321.333, 223.408, 260.868)), (' A 417  LYS  HD3', ' A 421  TYR  HD2', -0.4, (257.283, 258.896, 208.178)), (' B 575  ALA  HA ', ' B 586  ASP  HA ', -0.4, (259.595, 309.878, 273.008))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
