import gtk
import pango
import locale

class OperationDialog(gtk.Window):
	"""Dialog for operations

	Base class for operations dialog such as
	Copy/Move/Delete. Do *NOT* change this class
	as it might affect other dialogs and produce
	unpredictable behavior.

	"""

	def __init__(self, application, thread):
		gtk.Window.__init__(self, gtk.WINDOW_TOPLEVEL)

		self._paused = False
		self._application = application
		self._thread = thread
		self._size_format = '{0} / {1}'
		self._count_format = '{0} / {1}'
		self._has_details = False

		self._total_size = 0L
		self._total_count = 0L
		self._current_size = 0L
		self._current_count = 0L

		# set window properties
		self.set_title('Operation Dialog')
		self.set_default_size(400, 10)
		self.set_resizable(True)
		self.set_skip_taskbar_hint(True)
		self.set_transient_for(application)
		self.set_border_width(7)
		self.set_type_hint(gtk.gdk.WINDOW_TYPE_HINT_DIALOG)
		self.connect('destroy', self._destroy)

		# create interface
		self._vbox = gtk.VBox(False, 10)

		# operation items
		self._operation_label = gtk.Label()
		self._operation_label.set_alignment(0, 0.5)
		self._operation_progress = gtk.ProgressBar()

		vbox_operation = gtk.VBox(False, 0)
		vbox_operation.pack_start(self._operation_label, False, False, 0)
		vbox_operation.pack_start(self._operation_progress, False, False, 0)

		self._operation_item = self._application.add_operation(
															vbox_operation,
															self._operation_click
														)

		# pack interface
		self.add(self._vbox)

	def _add_source_destination(self):
		"""Add source and destination labels to the GUI"""
		frame = gtk.Frame()
		frame.set_shadow_type(gtk.SHADOW_OUT)

		table = gtk.Table(2, 2, False)
		table.set_border_width(7)
		table.set_col_spacing(0, 10)
		table.set_row_spacing(0, 2)

		self._label_source = gtk.Label(_('Source:'))
		self._label_destination = gtk.Label(_('Destination:'))

		self._value_source = gtk.Label()
		self._value_destination = gtk.Label()

		# pack interface
		table.attach(self._label_source, 0, 1, 0, 1, gtk.FILL)
		table.attach(self._label_destination, 0, 1, 1, 2, gtk.FILL)

		table.attach(self._value_source, 1, 2, 0, 1)
		table.attach(self._value_destination, 1, 2, 1, 2)

		frame.add(table)
		self._vbox.pack_start(frame, False, False, 0)

		# configure components
		self._label_source.set_alignment(0, 0.5)
		self._label_destination.set_alignment(0, 0.5)

		self._value_source.set_alignment(0, 0.5)
		self._value_destination.set_alignment(0, 0.5)
		self._value_source.set_ellipsize(pango.ELLIPSIZE_MIDDLE)
		self._value_destination.set_ellipsize(pango.ELLIPSIZE_MIDDLE)

	def _add_current_file(self):
		"""Add 'current file' progress to the GUI"""
		frame = gtk.Frame()
		frame.set_shadow_type(gtk.SHADOW_OUT)

		table = gtk.Table(2, 2, False)
		table.set_border_width(7)
		table.set_row_spacing(0, 2)

		self._label_status = gtk.Label('Current status...')
		self._label_current_file = gtk.Label()
		self._pb_current_file = gtk.ProgressBar()
		self._pb_current_file.set_pulse_step(0.005)

		# pack interface
		table.attach(self._label_status, 0, 1, 0, 1, gtk.FILL)
		table.attach(self._label_current_file, 1, 2, 0, 1)
		table.attach(self._pb_current_file, 0, 2, 1, 2)

		frame.add(table)
		self._vbox.pack_start(frame, False, False, 0)

		# configure components
		self._label_status.set_alignment(0, 0.5)
		self._label_current_file.set_alignment(1, 0.5)
		self._label_current_file.set_ellipsize(pango.ELLIPSIZE_MIDDLE)

	def _add_details(self):
		"""Add ETA to the dialog"""
		self._has_details = True
		frame = gtk.Frame()
		frame.set_shadow_type(gtk.SHADOW_OUT)

		table = gtk.Table(2, 6, False)
		table.set_border_width(7)

		self._label_eta = gtk.Label(_('ETA:'))
		self._label_speed = gtk.Label(_('Speed:'))
		self._label_total_size = gtk.Label(_('Total size:'))
		self._label_total_count = gtk.Label(_('Total count:'))

		self._value_eta = gtk.Label()
		self._value_speed = gtk.Label()
		self._value_total_size = gtk.Label()
		self._value_total_count = gtk.Label()

		self._pb_total_size = gtk.ProgressBar()
		self._pb_total_count = gtk.ProgressBar()

		# pack interface
		table.attach(self._label_eta, 0, 1, 0, 1, gtk.FILL)
		table.attach(self._label_speed, 0, 1, 1, 2, gtk.FILL)
		table.attach(self._label_total_size, 0, 1, 2, 3, gtk.FILL)
		table.attach(self._label_total_count, 0, 1, 4, 5, gtk.FILL)

		table.attach(self._value_eta, 1, 2, 0, 1)
		table.attach(self._value_speed, 1, 2, 1, 2)
		table.attach(self._value_total_size, 1, 2, 2, 3)
		table.attach(self._pb_total_size, 0, 2, 3, 4)
		table.attach(self._value_total_count, 1, 2, 4, 5)
		table.attach(self._pb_total_count, 0, 2, 5, 6)

		frame.add(table)
		self._vbox.pack_start(frame, False, False, 0)

		# configure components
		self._label_eta.set_alignment(0, 0.5)
		self._label_speed.set_alignment(0, 0.5)
		self._label_total_size.set_alignment(0, 0.5)
		self._label_total_count.set_alignment(0, 0.5)

		self._value_eta.set_alignment(0, 0.5)
		self._value_speed.set_alignment(0, 0.5)
		self._value_total_size.set_alignment(0, 0.5)
		self._value_total_count.set_alignment(0, 0.5)

		table.set_row_spacing(0, 2)
		table.set_row_spacing(1, 10)
		table.set_row_spacing(2, 2)
		table.set_row_spacing(3, 10)
		table.set_row_spacing(4, 2)
		table.set_col_spacing(0, 10)

	def _add_buttons(self):
		"""Add button bar"""
		hbox = gtk.HBox(False, 5)

		self._button_minimize = gtk.Button(_('Minimize'))
		self._button_pause = gtk.Button(_('Pause'))
		self._button_cancel = gtk.Button(_('Cancel'))

		self._button_minimize.connect('clicked', self._minimize_click)
		self._button_pause.connect('clicked', self._pause_click)
		self._button_cancel.connect('clicked', self._cancel_click)

		# pack interface
		hbox.pack_start(self._button_minimize, False, False, 0)
		hbox.pack_start(self._button_pause, False, False, 0)
		hbox.pack_end(self._button_cancel, False, False, 0)

		self._vbox.pack_end(hbox, False, False, 0)

	def _confirm_cancel(self, message):
		"""Create confirmation dialog with specified message and return result"""

		dialog = gtk.MessageDialog(self,
							gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION,
							gtk.BUTTONS_YES_NO, message)

		result = dialog.run()
		dialog.destroy()

		return result == gtk.RESPONSE_YES

	def _minimize_click(self, widget, data=None):
		"""Handle minimize click"""
		self._operation_item.show()
		self._application.operation_displayed()
		self.hide()

	def _pause_click(self, widget, data=None):
		"""Lock threading object"""
		self._paused = not self._paused

		if self._paused:
			self._button_pause.set_label(_('Resume'))
			self._thread.pause()
		else:
			self._button_pause.set_label(_('Pause'))
			self._thread.resume()

	def _cancel_click(self, widget, data=None):
		"""Handle cancel button click event"""
		if self._confirm_cancel(_('Are you sure about canceling current operation?')):
			self._thread.cancel()

	def _operation_click(self, widget, data=None):
		"""Handle operation menu item click"""
		self._operation_item.hide()
		self._application.operation_hidden()
		self.show()

	def _update_total_count(self):
		"""Update progress bar and labels for total count"""
		assert self._value_total_count is not None
		self._value_total_count.set_label(self._count_format.format(
															self._current_count,
															self._total_count
															))
		self.set_total_count_fraction(float(self._current_count) / self._total_count)

	def _update_total_size(self):
		"""Update progress bar and labels for total size"""
		assert self._value_total_size is not None
		self._value_total_size.set_label(self._size_format.format(
															locale.format('%d', self._current_size, True),
															locale.format('%d', self._total_size, True)
															))
		self.set_total_size_fraction(float(self._current_size) / self._total_size)

	def _destroy(self, widget, data=None):
		"""Remove operation menu item on dialog destroy"""
		self._application.remove_operation(self._operation_item)

	def set_status(self, status):
		"""Set current status"""
		assert self._label_status is not None
		self._label_status.set_label(status)
		self._operation_label.set_text(status)

	def set_current_file(self, path):
		"""Set current file name"""
		assert self._label_current_file is not None
		self._label_current_file.set_label(path)

	def set_current_file_fraction(self, fraction):
		"""Set current file progress bar position"""
		assert self._pb_current_file is not None
		self._pb_current_file.set_fraction(fraction)

		if not self._has_details:
			self._operation_progress.set_fraction(fraction)

	def set_current_count(self, count):
		"""Set current count value"""
		assert self._value_total_count is not None
		self._current_count = count
		self._update_total_count()

	def set_source(self, source):
		"""Set the content of source label"""
		assert self._value_source is not None
		self._value_source.set_label(source)

	def set_destination(self, destination):
		"""Set the content of destination label"""
		assert self._value_destination is not None
		self._value_destination.set_label(destination)

	def set_eta(self, eta):
		"""Set the content of eta label"""
		assert self._value_eta is not None
		self._value_eta.set_label(eta)

	def set_speed(self, speed):
		"""Set the content of speed label"""
		assert self._value_speed is not None
		self._value_speed.set_label(speed)

	def set_total_size(self, size):
		"""Set total size label"""
		assert self._value_total_size is not None
		self._value_total_size.set_label(size)

	def set_total_size_fraction(self, fraction):
		"""Set total size progress bar position"""
		assert self._pb_total_size is not None
		self._pb_total_size.set_fraction(fraction)
		self._operation_progress.set_fraction(fraction)

	def set_total_count(self, count):
		"""Set total count label"""
		assert self._value_total_count is not None
		self._total_count = count
		self._update_total_count()

	def set_total_count_fraction(self, fraction):
		"""Set total size progress bar position"""
		assert self._pb_total_count is not None
		self._pb_total_count.set_fraction(fraction)

	def increment_total_size(self, value):
		"""Increment total file size"""
		assert self._value_total_size is not None
		self._total_size += value
		self._update_total_size()

	def increment_current_size(self, value):
		"""Increment current summed file size"""
		assert self._value_total_size is not None
		self._current_size += value
		self._update_total_size()

	def increment_total_count(self, value):
		"""Increment total file count by value"""
		assert self._value_total_count is not None
		self._total_count += value
		self._update_total_count()

	def increment_current_count(self, value):
		"""Increment current file count by value"""
		assert self._value_total_count is not None
		self._current_count += value
		self._update_total_count()

	def pulse(self):
		"""Pulse current progress bar"""
		assert self._pb_current_file is not None
		self._pb_current_file.pulse()


class CopyDialog(OperationDialog):
	"""Dialog used to display progress for copying files"""

	def __init__(self, application, thread):
		OperationDialog.__init__(self, application, thread)

		# create additional controls
		self._add_source_destination()
		self._add_current_file()
		self._add_details()
		self._add_buttons()

		# configure layout
		self.set_title(_('Copy Selection'))


class MoveDialog(CopyDialog):
	"""Dialog used to display progress for moving files"""

	def __init__(self, application, thread):
		CopyDialog.__init__(self, application, thread)

		# configure layout
		self.set_title(_('Move Selection'))


class DeleteDialog(OperationDialog):
	"""Dialog displayed during delete procedure"""

	def __init__(self, application, thread):
		OperationDialog.__init__(self, application, thread)

		# create additional controls
		self._add_current_file()
		self._add_buttons()

		# configure layout
		self.set_title(_('Delete Selection'))
		self.set_status(_('Removing items...'))
		self.set_current_file('')
