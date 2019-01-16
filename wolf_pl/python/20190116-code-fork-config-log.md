## python - fork、config、log都操作
- **概述：**
>
>
>

- **log操作：**
>       logging.basicConfig(level=log_level,
                format='[%(levelname)s] [%(asctime)s] [%(filename)s:%(lineno)d] %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename= os.path.join(log_file_path, 'newlive_update_hostip.log'),
                filemode='a+')
        log = logging.getLogger()
>
>

- **fork操作：**
>       def daemon(stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
            try:
                pid = os.fork()
                if pid > 0:
                    # this parent, then exit
                    sys.exit(0)
            except Exception as e:
                sys.stderr.write("fork 1 failed, {0}\n".format(e))
                raise

            # this is the first forked child process
            # separate from parent's environment
            os.chdir('/')
            os.setsid()
            os.umask(0)

            try:
                pid = os.fork()
                if pid > 0:
                    sys.exit(0)
            except Exception as e:
                sys.stderr.write("fork 2 failed, {0}\n".format(e))
                raise

            # this is the second forded process
            # set fd
            sys.stdout.flush()
            sys.stderr.flush()
            stdin = file(stdin, 'r')
            stdout = file(stdout, 'a+')
            stderr = file(stderr, 'a+', 0)
            os.dup2(stdin.fileno(), sys.stdin.fileno())
            os.dup2(stdout.fileno(), sys.stdout.fileno())
            os.dup2(stderr.fileno(), sys.stderr.fileno())

        def main():
            try:
                domain_update = HandleDomainUpdate()
                update_time = int(time.time()) + update_on_time_interval
                while True:
                    if int(time.time()) >= update_time:
                        domain_update.run()
                        update_time = int(time.time()) + update_on_time_interval
                    time.sleep(1)
            except Exception as e:
                log.error('error {0}'.format(e))

        if __name__ == '__main__':
            opt = OptionParser()
            opt.add_option('-d',
                            action="store_true",
                            dest="is_daemon",
                            default=False,
                            help="run the scripts daemon")
            opts, args = opt.parse_args()
            if opts.is_daemon:
                daemon()
            main()
>
>
>
>
>
>
>
>
>
>
>

- **待续：**
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
>
