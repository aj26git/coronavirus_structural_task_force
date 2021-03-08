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
data['rota'] = [('A', '  86 ', 'VAL', 0.23642956891551598, (24.863999999999987, -9.205000000000007, -29.015)), ('A', ' 128 ', 'CYS', 0.15462327902233167, (4.312, -3.9170000000000003, -24.962000000000003)), ('A', ' 222 ', 'ARG', 0.06874565446164167, (-26.253999999999987, -8.408, -38.132)), ('A', ' 235 ', 'MET', 0.0, (-6.169999999999996, -1.9740000000000002, -45.569)), ('A', ' 238 ', 'ASN', 0.2131493049880406, (-3.8609999999999984, 1.084, -42.326)), ('A', ' 263 ', 'ASP', 0.06250363815431954, (-19.214, -11.875, -38.089)), ('B', '  27 ', 'LEU', 0.25020839144444607, (-7.026999999999997, -17.022, -1.297)), ('B', '  49 ', 'MET', 0.04634640635771409, (-21.452, -14.640000000000004, 4.364000000000001)), ('B', '  59 ', 'ILE', 0.13913817446903873, (-12.75, -17.853, 18.337000000000003)), ('B', '  62 ', 'SER', 0.02057832003147413, (-8.092999999999993, -23.323000000000004, 15.717)), ('B', ' 128 ', 'CYS', 0.253350717369899, (-3.635999999999999, 1.579, -10.544)), ('B', ' 277 ', 'ASN', 0.16272168088998357, (-11.263999999999994, 17.760000000000016, -32.305))]
data['cbeta'] = []
data['probe'] = [(' B  58  LEU HD22', ' B  82  MET  HE3', -0.833, (-10.164, -13.054, 13.353)), (' B 165  MET  HE1', ' B 187  ASP  HA ', -0.81, (-16.709, -6.971, 1.717)), (' B  86  VAL HG13', ' B 179  GLY  HA2', -0.648, (-7.525, -4.909, 6.753)), (' B 169  THR  OG1', ' B 171  VAL HG22', -0.616, (-17.371, -1.12, -9.633)), (' A  22 BCYS  SG ', ' A  61  LYS  NZ ', -0.533, (35.93, -0.957, -25.114)), (' A 222  ARG  NH2', ' A 503  HOH  O  ', -0.528, (-28.66, -2.221, -41.1)), (' B 294  PHE  CD1', ' B 298  ARG  NH1', -0.491, (7.155, 9.169, -8.103)), (' B  86  VAL HG13', ' B 179  GLY  CA ', -0.475, (-7.288, -4.858, 7.51)), (' A 113  SER  O  ', ' A 149  GLY  HA2', -0.472, (10.36, -7.725, -21.893)), (' B 207  TRP  CE2', ' B 288  GLU  HB2', -0.469, (-3.394, 10.381, -20.249)), (' B 126  TYR  HE2', ' B 128 ACYS  HG ', -0.468, (-5.251, -2.449, -10.923)), (' B 224  THR HG22', ' B 225  THR  N  ', -0.463, (-4.349, 31.799, -16.423)), (' B 155  ASP  HB3', ' B1004  EDO  H12', -0.454, (16.997, -0.363, -1.873)), (' A  90  LYS  HE2', ' A 406  EDO  H12', -0.443, (31.05, -18.258, -22.818)), (' B  27  LEU  C  ', ' B  27  LEU HD12', -0.44, (-5.849, -16.474, 0.155)), (' A  21  THR  HB ', ' A  67  LEU  HB3', -0.436, (32.397, -0.959, -16.518)), (' A 109  GLY  HA2', ' A 200  ILE HD13', -0.436, (0.832, -7.107, -32.935)), (' A  22 BCYS  HG ', ' A  61  LYS  HZ2', -0.433, (36.004, -0.397, -23.734)), (' A  22 ACYS  SG ', ' A  66  PHE  CD1', -0.432, (33.419, -3.824, -22.964)), (' A 233  VAL HG11', ' A 269  LYS  HG3', -0.414, (-14.58, -2.599, -43.655)), (' A 288  GLU  HG2', ' A 291  PHE  CE2', -0.41, (-5.994, -3.249, -25.03))]
handle_read_draw_probe_dots_unformatted("molprobity_probe.txt", 0, 0)
show_probe_dots(True, True)
gui = coot_molprobity_todo_list_gui(data=data)
