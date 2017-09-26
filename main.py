import subprocess
import os
import sys
import shutil
import time

MAP_LOCATIONS={"CH": "5.987549,47.788556,10.491943,45.818591"}
DEFAULT_MINZOOM=8
DEFAULT_MAXZOOM=16

#merge all gpx files in directory sub_dir/sports_type relative to script directory
def merge_gpx_files(sports_type, sub_dir="activities"):
    print("Merging gpx files of sport type %s" % sports_type)

    tmp_path = os.path.join(sub_dir,sports_type)

    #get a list of all files in directory sub_dir/sports_type
    files_list = os.listdir(tmp_path)

    #prepare the shell command as list of arguments, i.e. gpsbabel -i gpx -f file_dir -f ... -o gpx -F output_dir
    shell_command = ["gpsbabel", "-i", "gpx"]
    for file in files_list:
        if file.endswith(".gpx"):
            shell_command.extend(["-f", os.path.join(tmp_path,file)])

    #write merged gpx file to sub_dir
    shell_command.extend(["-o", "gpx", "-F", tmp_path+"_merged.gpx"])
    subprocess.call(shell_command)

    #return directory of merged file relative to script directory
    return sub_dir

def prepare_maperative_script(sports_type, regions, maxzoom=DEFAULT_MAXZOOM, sub_dir="activities"):
    print("Prepare Maperitive script for sport type %s" % sports_type)

    full_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), sub_dir) + os.sep

    try:
        os.remove("MaperitiveScript.mscript")
    except OSError:
        pass

    f = open("MaperitiveScript.mscript", "w+")
    f.write("load-source " + full_path + sports_type + "_merged.gpx\n")

    for region in regions:
        if region in MAP_LOCATIONS.keys():
            f.write("generate-tiles")
            f.write(" bounds="+MAP_LOCATIONS[region])
            f.write(" minzoom={} maxzoom={} ".format(DEFAULT_MINZOOM,maxzoom))
            f.write(" tilesdir=Tiles/"+region)
            f.write(" min-tile-file-size=700")

    f.close()

def remove_merged_gpx(sports_type, sub_dir="activities"):
    try:
        os.remove(sub_dir + os.sep + sports_type + "_merged.gpx")
    except OSError:
        pass

def remove_old_tiles():
    tmp_path = os.path.join("Maperitive", "Tiles")
    shutil.rmtree(tmp_path)
    os.makedirs(tmp_path)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sport_types = ["rides"]
    else:
        sport_types = sys.argv[1:]

    remove_old_tiles()

    # merge gpx data and create tiles
    for sport in sport_types:
        merge_gpx_files(sport)
        prepare_maperative_script(sport, ["CH"])

        print("Create tiles with Maperative for sport type" + sport)

        start_time=time.time()
        # run Maperitive script -> imports gpx files into Maperitive and render them end export as map-tiles
        subprocess.call("./runMaperitive.sh")
        elapsed_time = time.time()-start_time
        print(elapsed_time)

        remove_merged_gpx(sport)

        # run Mobile Atlas Creator
    #TODO subprocess.call("./MobileAtlasCreator/start.sh")

    #TODO remove_old_tiles()