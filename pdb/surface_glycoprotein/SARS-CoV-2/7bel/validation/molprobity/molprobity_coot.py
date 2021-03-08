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
data['omega'] = [('A', ' 155 ', 'PRO', None, (30.109000000000016, -69.042, 83.512)), ('A', ' 157 ', 'PRO', None, (31.765, -70.155, 77.572)), ('B', '   8 ', 'PRO', None, (12.956000000000003, -62.631, 52.28)), ('B', '  95 ', 'PRO', None, (21.725, -43.57099999999998, 64.268)), ('B', ' 141 ', 'PRO', None, (12.898999999999994, -81.503, 56.863)), ('C', ' 155 ', 'PRO', None, (21.04600000000001, -68.60499999999995, -27.698999999999998)), ('C', ' 157 ', 'PRO', None, (19.704, -69.989, -21.848)), ('D', '   8 ', 'PRO', None, (40.425, -62.86399999999998, 2.315)), ('D', '  95 ', 'PRO', None, (30.524000000000004, -43.562, -8.325)), ('D', ' 141 ', 'PRO', None, (40.017, -81.753, -2.823)), ('E', ' 108 ', 'PRO', None, (38.614, -9.609, 3.092)), ('H', ' 108 ', 'PRO', None, (14.278999999999996, -9.548999999999996, 51.37))]
data['rota'] = [('R', ' 387 ', 'LEU', 0.017206839205874718, (51.26899999999999, -42.293, 41.684)), ('R', ' 478 ', 'THR', 0.0027198671887163073, (15.322000000000024, -16.798, 73.219)), ('A', '  37 ', 'VAL', 0.03830207210965247, (28.848, -53.06599999999996, 68.729)), ('A', ' 156 ', 'GLU', 0.13558167085713269, (29.613000000000007, -69.732, 78.707)), ('H', '   2 ', 'LEU', 0.0, (10.280000000000001, -1.0969999999999998, 50.984)), ('H', '  13 ', 'LYS', 0.18925528173881848, (20.849000000000004, 24.611999999999984, 68.701)), ('H', '  31 ', 'SER', 0.027984301404198844, (7.413000000000004, -7.472999999999996, 60.456999999999994)), ('H', '  55 ', 'ASN', 0.2775034425135549, (11.427000000000007, -6.777999999999996, 69.161)), ('H', ' 119 ', 'GLN', 0.0, (18.009, 9.145000000000001, 51.967)), ('L', '   2 ', 'SER', 0.2843154373830252, (38.778999999999996, 2.9619999999999993, 63.57200000000001)), ('L', '   5 ', 'THR', 0.072671530005565, (41.275000000000006, -0.14500000000000005, 58.541999999999994)), ('L', '  98 ', 'VAL', 0.04275945271842471, (29.098000000000006, -1.5730000000000002, 68.099)), ('B', '  24 ', 'GLN', 0.10151962904806729, (14.168, -52.07599999999999, 51.889)), ('B', '  33 ', 'LEU', 0.10186193897266664, (24.283000000000023, -50.544, 52.17)), ('C', '  37 ', 'VAL', 0.003150532575091347, (23.409000000000006, -53.203, -11.999)), ('C', '  51 ', 'LEU', 0.17008379359037482, (18.346000000000004, -41.641, -12.077)), ('C', ' 187 ', 'SER', 0.03127525564114086, (26.660000000000007, -81.95099999999996, -20.354)), ('C', ' 218 ', 'LYS', 0.28968639093034704, (17.11200000000001, -92.21699999999998, -24.623)), ('E', '   2 ', 'LEU', 0.2469069463256052, (42.57300000000001, -1.095, 3.265)), ('E', '  55 ', 'ASN', 0.2963360482568637, (39.741, -7.236000000000001, -14.84)), ('E', ' 119 ', 'GLN', 0.0, (34.558, 8.916, 2.624)), ('F', '  98 ', 'VAL', 0.03941398518314028, (22.352, -2.07, -12.601)), ('D', '  21 ', 'ILE', 0.0027168045305473528, (36.844, -61.852, 5.721)), ('D', '  24 ', 'GLN', 0.0, (39.47600000000003, -52.3, 2.977)), ('D', '  33 ', 'LEU', 0.0025062211756695955, (29.348000000000027, -50.716, 3.846))]
data['cbeta'] = []
data['probe'] = [(' C   1  GLN  N  ', ' X 519  HIS  O  ', -0.822, (5.134, -55.442, -0.49)), (' F  38  GLN  HB2', ' F  48  LEU HD12', -0.765, (23.635, -1.606, 8.292)), (' R 383  SER  HB2', ' R 386  LYS  HG2', -0.744, (54.256, -37.844, 42.666)), (' R 403  ARG  HG3', ' R 405  ASP  OD1', -0.742, (31.75, -19.348, 44.653)), (' D  40  PRO  HG3', ' D 165  GLU  HG2', -0.741, (27.211, -72.012, -8.014)), (' L  38  GLN  HB2', ' L  48  LEU HD12', -0.734, (29.134, -1.001, 46.319)), (' D 105  ASP  OD1', ' D 106  ILE  N  ', -0.68, (34.341, -75.386, 0.714)), (' B 105  ASP  OD1', ' B 106  ILE  N  ', -0.665, (18.461, -75.856, 53.297)), (' X 383  SER  HB2', ' X 386  LYS  HG2', -0.661, (-0.054, -38.823, 17.504)), (' H  13  LYS  H  ', ' H  13  LYS  HD3', -0.656, (18.289, 23.708, 67.921)), (' A  51  LEU HD22', ' A  55  GLY  HA2', -0.654, (36.253, -38.928, 71.366)), (' E  41  GLN  HB2', ' E  47  LEU HD23', -0.65, (24.232, 7.143, -2.367)), (' C  34  MET  HB3', ' C  79  LEU HD22', -0.641, (14.978, -47.644, -11.914)), (' A  50  VAL HG21', ' A 105  TYR  HB3', -0.641, (30.934, -43.211, 64.124)), (' I   3  BMA  H2 ', ' I   6  MAN  H2 ', -0.636, (23.14, -15.573, -15.931)), (' B  38  GLN  NE2', ' B 302  HOH  O  ', -0.635, (23.494, -64.446, 63.257)), (' D 182  SER  OG ', ' D 185  ASP  OD2', -0.626, (39.616, -83.877, -37.911)), (' A  83  MET  HB3', ' A  86  LEU HD21', -0.61, (27.327, -52.569, 80.442)), (' H  41  GLN  HB2', ' H  47  LEU HD23', -0.598, (28.337, 7.823, 57.042)), (' A   1  GLN  N  ', ' R 519  HIS  O  ', -0.598, (48.078, -54.978, 58.245)), (' H  13  LYS  HE2', ' H  16  GLN  HG2', -0.588, (16.947, 22.971, 71.639)), (' E  99  ARG  HE ', ' E 115  ASP  HB3', -0.568, (36.057, -4.507, -0.018)), (' H  53  ILE HD13', ' H  73  VAL HG23', -0.56, (12.109, 1.424, 67.749)), (' C  50  VAL HG21', ' C 105  TYR  HB3', -0.55, (20.912, -43.213, -7.941)), (' C  83  MET  HB3', ' C  86  LEU HD21', -0.548, (23.319, -51.851, -24.544)), (' F  26  SER  HA ', ' F  30  GLY  HA3', -0.546, (13.451, -12.678, -8.387)), (' B 182  SER  OG ', ' B 185  ASP  OD2', -0.544, (10.739, -83.899, 91.796)), (' A  34  MET  HB3', ' A  79  LEU HD22', -0.54, (36.951, -47.843, 69.534)), (' C  35  HIS  HB2', ' C  97  ALA  HB3', -0.536, (19.092, -50.273, -8.535)), (' A  35  HIS  HB2', ' A  97  ALA  HB3', -0.536, (33.415, -50.052, 65.161)), (' L  14  PRO  HD3', ' L 111  GLY  H  ', -0.534, (41.542, 3.451, 33.359)), (' C  52  SER  O  ', ' C  72  ARG  NH1', -0.533, (13.476, -41.457, -10.892)), (' L   3  ALA  HB3', ' L 100  VAL HG11', -0.533, (36.648, -1.353, 64.138)), (' A  51  LEU HD21', ' A  58  LYS  HG2', -0.533, (33.033, -39.401, 72.768)), (' X 340  GLU  OE1', ' X 356  LYS  NZ ', -0.532, (23.892, -47.133, 15.845)), (' F 302  HOH  O  ', ' X 493  GLN  NE2', -0.532, (32.254, -15.997, 4.393)), (' H  70  THR  HB ', ' H  83  LYS  HB2', -0.52, (15.845, 9.967, 71.892)), (' E 102  SER  HB3', ' I   1  NAG  H82', -0.519, (30.729, -9.36, -7.558)), (' D 122  ASP  HA ', ' D 125  LEU  HB2', -0.517, (28.642, -91.719, -35.017)), (' A  73  ASP  OD1', ' A  75  SER  OG ', -0.513, (46.886, -41.97, 77.0)), (' E  53  ILE HD13', ' E  73  VAL HG23', -0.513, (39.557, 1.376, -13.855)), (' D  35  TRP  CE2', ' D  73  PHE  HB2', -0.51, (31.553, -58.099, 5.404)), (' X 393  THR  HA ', ' X 522  ALA  HA ', -0.508, (7.898, -52.527, 8.334)), (' B  22  THR HG22', ' B  72  THR HG22', -0.504, (15.434, -57.864, 46.276)), (' A 104  TYR  CZ ', ' R 355  ARG  HD2', -0.504, (32.815, -41.54, 53.704)), (' R 350  VAL HG22', ' R 422  ASN  HB3', -0.503, (30.111, -28.688, 51.74)), (' F  61  ASP  OD2', ' X 502  GLY  N  ', -0.501, (25.207, -13.853, 18.956)), (' E  35  ASN  HB2', ' E 100  HIS  HB3', -0.498, (31.942, -5.076, -7.585)), (' F 109  VAL HG13', ' F 112  GLN  HG2', -0.497, (15.481, 6.109, 20.22)), (' A  51  LEU HD12', ' A  70  ILE HG12', -0.495, (34.497, -43.849, 73.221)), (' D 147  GLN  HB3', ' D 154  LEU HD11', -0.493, (47.996, -84.356, -21.332)), (' D 145  LYS  HB3', ' D 197  THR  OG1', -0.493, (46.733, -83.316, -12.709)), (' L  26  SER  HA ', ' L  30  GLY  HA3', -0.491, (38.93, -11.789, 64.819)), (' D 108  ARG  NH1', ' D 111  ALA  HB2', -0.486, (35.887, -86.907, -0.366)), (' A 127  PRO  HB3', ' A 153  TYR  HB3', -0.484, (29.792, -76.765, 83.074)), (' B  35  TRP  HB2', ' B  48  ILE  HB ', -0.482, (26.625, -57.124, 50.545)), (' R 376  THR  O  ', ' R 434  ILE  HA ', -0.478, (41.33, -31.398, 40.807)), (' B  21  ILE HG21', ' B 102  THR HG21', -0.477, (17.697, -64.321, 52.268)), (' E  16  GLN  HG3', ' E  17  THR  H  ', -0.477, (33.953, 19.734, -18.415)), (' A  91  THR HG23', ' A 118  THR  HA ', -0.476, (25.872, -62.091, 79.473)), (' X 379  CYS  HA ', ' X 432  CYS  HA ', -0.473, (7.882, -34.41, 12.316)), (' G   1  NAG  H82', ' H 102  SER  HB3', -0.47, (20.633, -9.137, 62.555)), (' D  35  TRP  CD2', ' D  73  PHE  HB2', -0.47, (31.525, -58.765, 5.457)), (' H 100  HIS  NE2', ' H 112  TYR  O  ', -0.47, (23.875, -6.369, 58.952)), (' R 379  CYS  HA ', ' R 432  CYS  HA ', -0.468, (45.986, -33.801, 45.742)), (' C 208  HIS  CD2', ' C 210  PRO  HD2', -0.468, (16.575, -71.723, -25.326)), (' H  38  TRP  CE2', ' H  82  LEU  HB2', -0.466, (16.949, 8.078, 64.529)), (' E   4  LEU  HG ', ' E  24  VAL HG22', -0.464, (40.563, 2.201, -2.776)), (' X 412  PRO  HB3', ' X 426  PRO  O  ', -0.462, (8.263, -31.567, 2.203)), (' C 127  PRO  HB3', ' C 153  TYR  HB3', -0.461, (21.673, -76.184, -27.817)), (' R 401  VAL HG22', ' R 509  ARG  HG2', -0.461, (29.083, -30.424, 40.717)), (' A  67  ARG  HG2', ' A  84  ASN  O  ', -0.458, (24.112, -48.527, 83.035)), (' D  35  TRP  HB2', ' D  48  ILE  HB ', -0.458, (27.051, -57.23, 5.525)), (' C  67  ARG  HG2', ' C  84  ASN  O  ', -0.457, (26.959, -47.875, -26.541)), (' D 207  LYS  HA ', ' D 207  LYS  HD3', -0.456, (40.075, -95.744, -17.885)), (' C 104  TYR  CZ ', ' X 355  ARG  HD2', -0.456, (20.508, -41.856, 2.897)), (' H  16  GLN  HG3', ' H  17  THR  H  ', -0.455, (16.807, 20.669, 72.57)), (' L  50  TYR  O  ', ' L  54  LEU  HB2', -0.45, (26.573, -12.629, 51.603)), (' X 357  ARG  HG3', ' X 396  TYR  CE1', -0.449, (17.421, -47.238, 6.368)), (' L  48  LEU HD21', ' L  63  PHE  CG ', -0.449, (30.06, -5.439, 44.388)), (' E  54  TYR  CZ ', ' I   1  NAG  H62', -0.449, (32.697, -7.125, -16.201)), (' R 358  ILE  HB ', ' R 395  VAL  HB ', -0.447, (40.159, -45.699, 46.312)), (' B  50  ASP  OD1', ' B  91  TYR  OH ', -0.445, (29.347, -48.532, 51.266)), (' R 376  THR  HB ', ' R 435  ALA  HB3', -0.444, (39.194, -28.069, 41.037)), (' H  61  TYR  HB2', ' H  66  LYS  HG3', -0.444, (23.268, 3.413, 74.854)), (' B 108  ARG  NH1', ' B 111  ALA  HB2', -0.443, (16.85, -87.056, 54.508)), (' D 193  ALA  HB2', ' D 208  SER  HB3', -0.442, (42.922, -94.455, -22.302)), (' E  70  THR  HB ', ' E  83  LYS  HB2', -0.438, (35.308, 9.757, -17.893)), (' C  37  VAL HG13', ' C  47  TRP  HA ', -0.436, (25.339, -51.892, -10.273)), (' X 373  SER  O  ', ' X 373  SER  OG ', -0.435, (17.726, -30.341, 24.756)), (' A  18  LEU  HB3', ' A  83  MET  HE3', -0.434, (30.324, -53.941, 81.428)), (' E  38  TRP  CE2', ' E  82  LEU  HB2', -0.432, (34.818, 7.558, -10.271)), (' C  22  CYS  HB3', ' C  79  LEU  HB3', -0.432, (13.146, -50.19, -14.244)), (' D  61  ARG  NH1', ' D  82  ASP  OD2', -0.431, (26.262, -70.444, 7.915)), (' A 179  GLN  HA ', ' B 160  GLN HE22', -0.431, (16.603, -73.421, 81.863)), (' X 350  VAL HG22', ' X 422  ASN  HB3', -0.43, (22.931, -28.845, 4.547)), (' G   1  NAG  H62', ' H  54  TYR  CE1', -0.429, (18.488, -6.183, 70.465)), (' R 395  VAL HG22', ' R 515  PHE  HD1', -0.429, (44.291, -44.053, 47.376)), (' L  81  SER  OG ', ' L 112  GLN  OE1', -0.427, (35.169, 5.508, 33.042)), (' B  91  TYR  HA ', ' B  96  LEU HD22', -0.426, (25.676, -46.527, 58.776)), (' B 147  GLN  HB3', ' B 154  LEU HD11', -0.426, (3.208, -84.341, 74.625)), (' R 341  VAL  CG2', ' R 356  LYS  HD3', -0.425, (33.403, -43.394, 42.624)), (' A  47  TRP  HD1', ' A 108  MET  CE ', -0.425, (28.59, -49.347, 64.888)), (' F 110  LEU  HA ', ' F 110  LEU HD12', -0.424, (10.786, 6.335, 19.122)), (' R 387  LEU  O  ', ' R 387  LEU HD12', -0.423, (49.801, -44.007, 42.404)), (' G   4  MAN  O2 ', ' G   5  MAN  H2 ', -0.423, (25.143, -21.525, 76.762)), (' D  12  SER  HB3', ' D 105  ASP  HB3', -0.423, (37.607, -74.274, 0.819)), (' R 493  GLN  HG3', ' R 494  SER  N  ', -0.422, (21.108, -20.902, 49.662)), (' E   4  LEU HD23', ' E  22  CYS  SG ', -0.419, (38.141, 4.077, -3.969)), (' H  11  LEU HD23', ' H 124  THR  HB ', -0.419, (22.857, 23.171, 60.374)), (' B  35  TRP  CE2', ' B  73  PHE  HB2', -0.418, (22.019, -58.233, 49.945)), (' E 110  TYR  CE2', ' F  56  PRO  HB3', -0.416, (32.275, -8.31, 6.669)), (' B  33  LEU HD11', ' B  88  CYS  HB2', -0.416, (21.451, -54.211, 53.462)), (' A 173  THR HG23', ' A 188  SER  HB2', -0.415, (28.793, -81.465, 73.012)), (' F  53  ASP  OD1', ' X 417  LYS  NZ ', -0.414, (22.996, -16.115, 2.737)), (' B  88  CYS  O  ', ' B  99  GLY  N  ', -0.413, (20.228, -54.554, 58.472)), (' A  37  VAL HG13', ' A  47  TRP  HA ', -0.41, (26.578, -51.64, 66.998)), (' D 124  GLN HE22', ' D 131  SER  CB ', -0.41, (31.339, -84.279, -29.471)), (' A   1  GLN  N  ', ' R 520  ALA  HA ', -0.409, (47.574, -55.207, 57.749)), (' F  12  GLU  HG3', ' F  18 BVAL HG23', -0.409, (10.729, -1.682, 14.581)), (' F  12  GLU  HG3', ' F  18 AVAL HG23', -0.409, (10.729, -1.682, 14.581)), (' A  51  LEU HD23', ' A  57  ASN  O  ', -0.408, (33.3, -39.066, 70.689)), (' L 112  GLN  HA ', ' L 113  PRO  HD3', -0.408, (37.918, 7.79, 31.152)), (' A 131  PRO  HD3', ' A 217  LYS  HE2', -0.407, (29.133, -89.744, 83.626)), (' H   4  LEU HD23', ' H  22  CYS  SG ', -0.404, (14.284, 4.048, 58.049)), (' D 115  VAL  HA ', ' D 135  LEU  O  ', -0.404, (35.897, -89.61, -14.167)), (' E  40  ARG  HB3', ' E  50  ILE HD11', -0.403, (27.582, 8.725, -8.447)), (' H  99  ARG  HE ', ' H 115  ASP  HB3', -0.402, (16.379, -4.148, 54.449)), (' B 115  VAL  HA ', ' B 135  LEU  O  ', -0.402, (16.001, -89.291, 68.705)), (' X 399  SER  HA ', ' X 510  VAL  O  ', -0.401, (20.66, -34.395, 12.763)), (' X 401  VAL HG22', ' X 509  ARG  HG2', -0.401, (24.971, -30.516, 16.048)), (' F  29  ILE  O  ', ' F  67  LYS  HE3', -0.401, (16.32, -13.085, -4.387)), (' G   1  NAG  H62', ' H  54  TYR  CZ ', -0.4, (18.257, -6.481, 70.702)), (' C  60  TYR  CE1', ' C  70  ILE HG22', -0.4, (21.264, -43.125, -17.281)), (' I   3  BMA  C2 ', ' I   6  MAN  H2 ', -0.4, (23.242, -15.264, -16.471))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
