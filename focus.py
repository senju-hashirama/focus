#! /bin/python
import os
import argparse
from pathlib import Path

def main(gargs):

    if gargs.List:
        with open("/etc/hosts","r+") as host:
            data=host.readlines()
        if "#Focus\n" in data:
            hosts=data.index("#Focus\n")+1
            if "#" in data[hosts]:
                data[hosts]=data[hosts][1:]
            
            for i in data[hosts].split()[1:]:
                 print(i)
            
        return
    
    if gargs.Remove:
        with open("/etc/hosts","r+") as host:
            data=host.readlines()
            if "#Focus\n" in data:
                hosts=data.index("#Focus\n")+1
                if gargs.Remove in data[hosts]:
                    temp=data[hosts].split()
                    temp.remove(gargs.Remove)
                    data[hosts]=" ".join(temp)

            host.seek(0,0)
            host.writelines(data)
            host.truncate()
            return
                
            

    #Set focus
    if gargs.Deactivate:

        #read /etc/hosts file
        with open("/etc/hosts","r+") as host:
            data=host.readlines()
            host.seek(0, 2)

            sites = ["www.instagram.com"]

            #read input file
            if gargs.File:
                try:
                    with open(Path(args.File), "r") as f:
                        sites = f.readlines()
                        sites=[i.strip() for i in sites]
                        print(sites)
                except FileNotFoundError:
                    print("Invalid input file path")
        
            # Check if we have modified /etc/hosts file   
            if "#Focus\n" not in data:
                    # Add single entry and exit
                    if gargs.Site:
                        print("Inserting single entry")
                        host.write("#Focus\n")
                        host.write("127.0.0.1 {}\n".format(gargs.Site))
                        return

                    print("inserting new data")
                    host.write("#Focus\n")
                    host.write("127.0.0.1 {}\n".format(" ".join(sites)))
                    print("Done writing ", "127.0.0.1 {}".format(" ".join(sites)))
                    return


            
            else:
                    hosts = data.index("#Focus\n") + 1

                    #Add single site entry to the end of existing line
                    if gargs.Site:
                        if gargs.Site not in [i.strip() for i in data[hosts].split()[1:]]:
                            data[hosts]=data[hosts].strip()+" {}".format(gargs.Site)
                            host.seek(0)
                            host.writelines(data)
                            host.truncate()
                            return
                    

                        


                    #Check if the existing entries are same as the one we read from input file if we have specified any
                    if gargs.File:
                        if [i.strip() for i in data[hosts][1:].split()[1:]]!=sites:
                                print("resetting")
                                data[hosts]="127.0.0.1 {}\n\n".format(" ".join(sites))
                                
                        
                    
                    # Check if we have commented previous line and uncomment it
                    # This enables us to keep our previous configuration
                    if data[hosts][0]=="#":
                                data[hosts]=data[hosts][1:]

                    host.seek(0,0)
                    host.writelines(data)
                    return

    #Disable focus
    else:
            with open("/etc/hosts","r+") as host:
                data=host.readlines()
                host.seek(0, 2)
                print("Removing")
                try:
                    hosts = data.index("#Focus\n") + 1
                    if data[hosts][0]!="#":
                            data[hosts] = "#" + data[hosts]
                            host.seek(0,0)
                            host.writelines(data)
                except ValueError as e:
                    print(e)
                except Exception as e:
                    print(e)
                return


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--File", help="Text file with all domains to block")
    parser.add_argument("-d", "--Deactivate", help="Deactivate focus", action="store_false") #Default value of args.Deactivate is True and when -d is passed it becomes False
    parser.add_argument("-s","--Site",help="Block a particular website")
    parser.add_argument("-l","--List",help="List all blocked sites",action="store_true")
    parser.add_argument("-rm","--Remove",help="Remove a site from blocked list")
    args = parser.parse_args()
    print(args)
    main(args)
