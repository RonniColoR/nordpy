#!/usr/bin/python3

from bin.gui_components.root_password_window import RootPermissionWindow
import os
import argparse


def get_parser():
    parser = argparse.ArgumentParser(prog="nordpy",
                                     description='An application to connect to NordVPN servers')
    connection_group = parser.add_mutually_exclusive_group()

    connection_group.add_argument('--quick-connect', action="store_true",
                        help='connects to the last chosen server type')
    connection_group.add_argument('--quick-disconnect', action="store_true",
                        help='disconnect nordpy VPN connection')

    return parser


def main():
    # if file is launched without root privileges
    parser = get_parser()
    parsed_args = parser.parse_args()

    if parsed_args.quick_connect:
        from bin.command_line_util import quick_connect
        quick_connect()
    elif parsed_args.quick_disconnect:
        from bin.command_line_util import quick_disconnect
        quick_disconnect()

    elif os.geteuid() != 0:
        root_request_win = RootPermissionWindow()
        root_request_win.mainloop()
        # checking if a correct password has been inserted
        from bin.gui_components.root_password_window import password_inserted

        if password_inserted is None:
            return

        import bin.root
        bin.root.get_root_permissions(password_inserted)
        del password_inserted

        from bin.gui import gui
        app = gui()
        app.mainloop()


if __name__ == "__main__":
    main()
