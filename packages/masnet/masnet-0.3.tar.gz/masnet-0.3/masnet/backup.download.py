# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
# pylint: disable=global-statement
# pylint: disable=bare-except,broad-except
import argparse
from collections import deque
import datetime
import json
import math
import os
import socket
import time
from threading import Thread, Lock
import traceback
from urllib.error import URLError, HTTPError
import urllib.request
from masnet import get_peers_file_path, get_error_file_path, load_exclusion
from masnet import get_version, set_verbose, set_working_dir, debug
from masnet import set_debug, is_excluded, get_path, is_debug, is_verbose
from masnet import get_excluded_patterns


THREADS_RUN = True

num_domains = 0
num_timeouts = 0
num_errors = 0
num_errors_lock = Lock()
num_skips = 0
num_downloads = 0
avg_download = 0
sum_download = 0
len_qerror = 0
len_qskip = 0
len_qdecode = 0
len_qprocess = 0

def get_thread_status(t_decode,
                      t_process,
                      t_error_handler,
                      t_skip_handler,
                      t_downloads):
    num_alives = 0
    for t in t_downloads:
        if t.is_alive():
            num_alives = num_alives + 1
    p = math.ceil(10*num_alives/len(t_downloads))
    return '%s%s%s%s%s' % ('A' if t_error_handler.is_alive() else '.',
                           'A' if t_skip_handler.is_alive() else '.',
                           '.' if num_alives == 0 else ('A' if p == 10 else str(p)),
                           'A' if t_decode.is_alive() else '.',
                           'A' if t_process.is_alive() else '.')


def are_all_download_threads_alive(t_downloads):
    for t in t_downloads:
        if not t.is_alive():
            return False
    return True

def is_any_download_thread_alive(t_downloads):
    for t in t_downloads:
        if t.is_alive():
            return True
    return False

# pylint: disable=unused-argument
def skip_handler(idx,
                 qskip,
                 skips_filepath):

    global THREADS_RUN, num_skips, len_qskip

    with open(skips_filepath, 'w') as fp:
        try:
            while THREADS_RUN:
                time.sleep(0)
                try:
                    len_qskip = max(len_qskip, len(qskip))
                    req = qskip.popleft()
                    domain = req['domain']
                    num_skips = num_skips + 1
                    fp.write(domain)
                    fp.write('\n')
                except IndexError:
                    pass
        except:
            traceback.print_exc()

# pylint: disable=unused-argument
def error_handler(idx,
                  qerror,
                  errors_filepath):

    global THREADS_RUN, num_errors, num_errors_lock
    global len_qerror

    with open(errors_filepath, 'w') as fp:
        try:
            while THREADS_RUN:
                time.sleep(0)
                try:
                    len_qerror = max(len_qerror, len(qerror))
                    req = qerror.popleft()
                    domain = req['domain']
                    with num_errors_lock:
                        num_errors = num_errors + 1
                    err = req['err']
                    fp.write(domain)
                    fp.write('\n')
                    error_file_path = get_error_file_path(domain)
                    with open(error_file_path, 'w') as f:
                        f.write(err)
                except IndexError:
                    pass
        except:
            traceback.print_exc()

# pylint: disable=too-many-arguments
# pylint: disable=too-many-branches
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements
def download(idx,
             qerror,
             qdownload,
             qdecode,
             qprocess,
             dtimes,
             discard,
             timeout=-1):

    global THREADS_RUN
    global num_downloads, avg_download, sum_download, num_timeouts
    global num_errors, num_errors_lock

    # pylint: disable=too-many-nested-blocks
    try:
        while THREADS_RUN:
            time.sleep(0)
            try:
                req = qdownload.popleft()
                domain = req['domain']
                error_file_path = get_error_file_path(domain)
                if os.path.exists(error_file_path):
                    with num_errors_lock:
                        num_errors = num_errors + 1
                    continue
                # if not discarding, try to load existing file first
                if not discard:
                    peers_file_path = get_peers_file_path(domain)
                    if os.path.exists(peers_file_path):
                        try:
                            with open(peers_file_path, 'rb') as f:
                                res = json.load(f)
                                qprocess.append({'domain': domain,
                                                 'peers': res['peers']})
                                continue
                        except:
                            pass
                peers_url = 'https://%s/api/v1/instance/peers' % domain
                res = None
                err = None
                elapsed = -1
                try:
                    num_downloads = num_downloads + 1
                    start = time.perf_counter()
                    if timeout > 0:
                        with urllib.request.urlopen(peers_url,
                                                    timeout=timeout) as req:
                            res = req.read().decode('utf-8')
                    else:
                        with urllib.request.urlopen(peers_url) as req:
                            res = req.read().decode('utf-8')
                    elapsed = time.perf_counter() - start
                    dtimes.append((domain, elapsed))
                    sum_download = sum_download + elapsed
                    avg_download = sum_download / num_downloads
                except HTTPError as e:
                    err = '%s %s' % (e.__class__.__name__, e.code)
                except URLError as e:
                    err = '%s %s' % (e.__class__.__name__, e.reason)
                # this became an alias to TimeoutError
                except socket.timeout as e:
                    num_timeouts = num_timeouts + 1
                    err = e.__class__.__name__
                except TimeoutError as e:
                    num_timeouts = num_timeouts + 1
                    err = e.__class__.__name__
                except ConnectionError as e:
                    err = e.__class__.__name__
                except UnicodeError as e:
                    err = e.__class__.__name__
                if err is not None:
                    qerror.append({'domain': domain, 'err': err})
                elif res is not None:
                    qdecode.append({'domain': domain,
                                    'elapsed': elapsed,
                                    'peers_json': res})
                else:
                    raise Exception('why res is None?')
            except IndexError as e:
                pass
    except:
        traceback.print_exc()


def decode(idx,
           qerror,
           qdecode,
           qprocess,
           visits_filepath):

    global THREADS_RUN, len_qdecode

    with open(visits_filepath, 'w') as fp:
        try:
            while THREADS_RUN:
                time.sleep(0)
                try:
                    len_qdecode = max(len_qdecode, len(qdecode))
                    req = qdecode.popleft()
                    domain = req['domain']
                    elapsed = req['elapsed']
                    peers_file_path = get_peers_file_path(domain)
                    try:
                        peers = json.loads(req['peers_json'])
                        peers_json = {'domain': domain,
                                      'elapsed': elapsed,
                                      'peers': peers}
                        with open(peers_file_path, 'wb') as f:
                            f.write(json.dumps(peers_json).encode('utf-8'))
                        fp.write(domain)
                        fp.write('\n')
                        qprocess.append({'domain': domain, 'peers': peers})
                    except json.JSONDecodeError as e:
                        err = e.__class__.__name__
                        qerror.append({'domain': domain, 'err': err})
                except IndexError as e:
                    pass
        except:
            traceback.print_exc()


def process(idx,
            qerror,
            qskip,
            qprocess,
            qdownload,
            start_domain):

    global THREADS_RUN, num_domains, len_qprocess

    domains = set()

    # send start domain
    domains.add(start_domain)
    qdownload.append({'domain': start_domain})

    # pylint: disable=too-many-nested-blocks
    try:
        while THREADS_RUN:
            time.sleep(0)
            try:
                len_qprocess = max(len_qprocess, len(qprocess))
                req = qprocess.popleft()
                num_domains = num_domains + 1
                peers = req['peers']
                for peer in peers:
                    # this is not needed, but just to handle bad responses safely
                    if peer is not None and len(peer) > 0:
                        if is_excluded(peer):
                            qskip.append({'domain': peer})
                        elif peer not in domains:
                            domains.add(peer)
                            qdownload.append({'domain': peer})
            except IndexError:
                pass
    except:
        traceback.print_exc()


# pylint: disable=too-many-statements
def main():
    print('masnet v%s' % get_version())
    parser = argparse.ArgumentParser(prog='masnet.download',
                                     description='',
                                     epilog='')

    parser.add_argument('-d', '--dir',
                        help='use specified directory for files',
                        required=False)

    parser.add_argument('--debug',
                        help='enables debug logging',
                        action='store_true',
                        required=False,
                        default=False)

    parser.add_argument('-v', '--verbose',
                        help='enable verbose logging, mostly for development',
                        action='store_true',
                        required=False,
                        default=False)

    parser.add_argument('--discard',
                        help='discard cached peers.json files, ' \
                             'redownloads everything (default: false)',
                        action='store_true',
                        required=False,
                        default=False)

    parser.add_argument('-e', '--exclude-file',
                        help='exclude the domains and all of their ' \
                             'subdomains in the file specified',
                        required=False)

    cpu_count = 0
    try:
        cpu_count = os.cpu_count()
    except:
        cpu_count = 4

    parser.add_argument('-n', '--num-threads',
                        help='use specified number of Python threads for download',
                        type=int,
                        required=False,
                        default=cpu_count*8)

    parser.add_argument('-s', '--start-domain',
                        help='domains to start traversal from (default: mastodon.social)',
                        required=False,
                        default='mastodon.social')

    parser.add_argument('-t', '--timeout',
                        help='use specified number of seconds for timeout ' \
                             '(default: system default)',
                        type=int,
                        required=False,
                        default=-1)

    args = parser.parse_args()
    set_debug(args.debug)
    set_verbose(args.verbose)
    debug(str(args))
    load_exclusion(args.exclude_file)
    set_working_dir(args.dir)

    # reset files
    errors_filepath = get_path('masnet.download.errors')
    skips_filepath = get_path('masnet.download.skips')
    visits_filepath = get_path('masnet.download.visits')

    print('starting threads...')

    qerror = deque()
    qdownload = deque()
    qdecode = deque()
    qprocess = deque()
    qskip = deque()
    dtimes = deque()

    t_downloads = list()

    for i in range(0, args.num_threads):
        t_downloads.append(Thread(name='masnet.download.%d' % i,
                                  target=download,
                                  args=[i,
                                        qerror,
                                        qdownload,
                                        qdecode,
                                        qprocess,
                                        dtimes,
                                        args.discard,
                                        args.timeout]))

    t_decode = Thread(name='masnet.decode',
                      target=decode,
                      args=[i,
                            qerror,
                            qdecode,
                            qprocess,
                            visits_filepath])

    t_process = Thread(name='masnet.process',
                       target=process,
                       args=[0,
                             qerror,
                             qskip,
                             qprocess,
                             qdownload,
                             args.start_domain])

    t_error_handler = Thread(name='masnet.error_handler',
                             target=error_handler,
                             args=[0,
                                   qerror,
                                   errors_filepath])

    t_skip_handler = Thread(name='masnet.skip_handler',
                            target=skip_handler,
                            args=[0,
                                  qskip,
                                  skips_filepath])

    t_error_handler.start()
    t_skip_handler.start()
    for t_download in t_downloads:
        t_download.start()
    t_decode.start()
    t_process.start()

    global THREADS_RUN
    global num_domains, num_errors, num_skips

    def print_status(start):
        elapsed = time.time() - start
        hours = int(elapsed / 3600)
        minutes = int((elapsed - hours * 3600) / 60)
        seconds = elapsed - minutes * 60 - hours * 3600
        status = 'd:%06d e:%06d s:%08d qd:%08d ' \
            't:%02d:%02d:%02d ' \
            'da:%d to:%d' % (num_domains,
                             num_errors,
                             num_skips,
                             len(qdownload),
                             hours, minutes, seconds,
                             int(avg_download*1000), num_timeouts)
        print(status)
        if is_verbose():
            extra = 'qmax:%02d/%02d/%02d/%02d ' \
                'qlen:%02d/%02d/%02d/%02d ' % (len_qskip, len_qerror, len_qdecode, len_qprocess,
                                               len(qskip), len(qerror), len(qdecode), len(qprocess))
            print(extra)
        return status

    start = time.time()

    len_zero = 0

    try:
        while True:
            if not t_decode.is_alive():
                print('decode thread terminated unexpectedly, quitting...')
                break
            if not t_process.is_alive():
                print('process thread terminated unexpectedly, quitting...')
                break
            if not t_error_handler.is_alive():
                print('error handler thread terminated unexpectedly, quitting...')
                break
            if not t_skip_handler.is_alive():
                print('skip handler thread terminated unexpectedly, quitting...')
                break
            if not are_all_download_threads_alive(t_downloads):
                print('at least one download thread terminated unexpectedly, quitting...')
                break
            print_status(start)
            if len(qdownload) == 0:
                len_zero = len_zero + 1
            else:
                len_zero = 0
            if len_zero == 5:
                print('nothing left in download queue, finished.')
                break
    except KeyboardInterrupt:
        pass

    print('wait for threads to terminate...')
    # terminate threads
    THREADS_RUN = False

    # wait until they are all terminated
    while (t_decode.is_alive() or
           t_process.is_alive() or
           t_error_handler.is_alive() or
           t_skip_handler.is_alive() or
           is_any_download_thread_alive(t_downloads)):
        print(get_thread_status(t_decode,
                                t_process,
                                t_error_handler,
                                t_skip_handler,
                                t_downloads))
        time.sleep(1)

    # write final state
    print(get_thread_status(t_decode,
                            t_process,
                            t_error_handler,
                            t_skip_handler,
                            t_downloads))
    status = print_status(start)

    print('saving status to masnet.download.log')
    with open(get_path('masnet.download.log'), 'w') as f:
        f.write('%s\n' % datetime.datetime.now().isoformat())
        f.write('%s\n' % str(args))
        f.write('%s\n' % status)
        f.write('List of excluded patterns:')
        for excluded_pattern in get_excluded_patterns():
            f.write('%s\n' % excluded_pattern)

    if is_debug():
        print('saving download queue to masnet.download.qdownload')
        with open(get_path('masnet.download.qdownload'), 'w') as f:
            try:
                while True:
                    doc = qdownload.popleft()
                    f.write(doc['domain'])
                    f.write('\n')
            except IndexError:
                pass

    print('saving download times to masnet.download.times')
    with open(get_path('masnet.download.times'), 'w') as f:
        try:
            while True:
                (domain, dt) = dtimes.popleft()
                f.write('%d %s' % (int(dt*1000), domain))
                f.write('\n')
        except IndexError:
            pass

    print('bye.')

if __name__ == '__main__':
    main()
