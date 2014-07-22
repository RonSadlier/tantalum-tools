'''
Copyright 2014 Ronald Sadlier

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import signal, subprocess
from locale import getdefaultlocale
from os import kill
from sys import argv

def kTa(terms):
    """Kill processes with a name that contains at least one term"""
    out = subprocess.Popen(['ps', '-A'],
                           stdout=subprocess.PIPE).communicate()[0]

    # The PIDs of processes that match any of our search terms
    pids = [ int(line.split(None, 1)[0])
             for line in out.decode(getdefaultlocale()[1]).splitlines()
             if any(term in line for term in terms) ]
    # If we have any PIDs then lazy evaluate kill them
    if len(pids) and [ kill(pid, signal.SIGKILL) for pid in pids ]:
        return pids

if __name__ == '__main__':
    pids = kTa(argv[1:])

    if pids is not None:
         print("We killed PID(s): ", pids)
