''' log_man.py

central location to configure and manage the logging system.
ideally all other modules should get their logger from this module.
Here you can swtich the logging backend, or any additional configuration.

'''

from libr3dv1t.log_utilz import simple_log as current_logger
