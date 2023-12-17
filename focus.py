#! /bin/python
import os
import argparse
from pathlib import Path

def main(gargs):
    
    if gargs.Deactivate:
        
        sites = ["www.instagram.com"]
        if gargs.File:
            try:
                with open(Path(args.File), "r") as f:
                    sites = f.readlines()
                    sites=[i.strip() for i in sites]
                    print(sites)
            except FileNotFoundError:
                print("Invalid input file path")
        with open("/etc/hosts", "r+") as host:
            data = host.readlines()
            host.seek(0, 2)
            if "#Focus\n" not in data:
                print("inserting new data")
                host.write("#Focus\n")
                host.write("127.0.0.1 {}\n".format(" ".join(sites)))
                print("Done writing ", "127.0.0.1 {}".format(" ".join(sites)))
            else:
                hosts = data.index("#Focus\n") + 1
                data[hosts] = data[hosts][1:]
                if [i.strip() for i in data[hosts].split()[1:]]!=sites:
                         print("resetting")
                         host.seek(0)
                         data[hosts]="127.0.0.1 {}\n\n".format(" ".join(sites))
                         host.writelines(data)
                         host.truncate()
                else:
                   print(data)
                   host.seek(0,0)
                   host.writelines(data)

    else:
        print("Removing")
        with open("/etc/hosts", "r+") as host:
            data = host.readlines()
            try:
                
                hosts = data.index("#Focus\n") + 1
                if data[hosts][0]!="#":
                        data[hosts] = "#" + data[hosts]
                        host.seek(0,0)
                        host.writelines(data)
            except ValueError:
                pass
            except Exception as e:
                print(e)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--File", help="Text file with all domains to block")
    parser.add_argument("-d", "--Deactivate", help="Deactivate focus", action="store_false")
    parser.add_argument("-s","--Site",help="Block a particular website")
    args = parser.parse_args()
    main(args)
