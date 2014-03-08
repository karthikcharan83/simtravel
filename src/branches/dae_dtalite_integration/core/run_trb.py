import os

if __name__ == "__main__":
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone1/config_before_malta.xml -it 1 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone1/config_after_malta.xml -it 1 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("cp /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_1/worker.txt")
    os.system("cp /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_1/worker.txt")

    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone2/config_before_malta.xml -it 2 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone2/config_after_malta.xml -it 2 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("cp /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_2/worker.txt")
    os.system("cp /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_2/worker.txt")

    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone3/config_before_malta.xml -it 3 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone3/config_after_malta.xml -it 3 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_3/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_3/worker.txt")

    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone4/config_before_malta.xml -it 4 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone4/config_after_malta.xml -it 4 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_4/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_4/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone5/config_before_malta.xml -it 5 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone5/config_after_malta.xml -it 5 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_5/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_5/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone6/config_before_malta.xml -it 6 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone6/config_after_malta.xml -it 6 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_6/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_6/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone7/config_before_malta.xml -it 7 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone7/config_after_malta.xml -it 7 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_7/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_7/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone8/config_before_malta.xml -it 8 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone8/config_after_malta.xml -it 8 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_8/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_8/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone9/config_before_malta.xml -it 9 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone9/config_after_malta.xml -it 9 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_9/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_9/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone10/config_before_malta.xml -it 10 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone10/config_after_malta.xml -it 10 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_10/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_10/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone11/config_before_malta.xml -it 11 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone11/config_after_malta.xml -it 11 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_11/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_11/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone12/config_before_malta.xml -it 12 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone12/config_after_malta.xml -it 12 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_12/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_12/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone13/config_before_malta.xml -it 13 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone13/config_after_malta.xml -it 13 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_13/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_13/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone14/config_before_malta.xml -it 14 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone14/config_after_malta.xml -it 14 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_14/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_14/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone15/config_before_malta.xml -it 15 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone15/config_after_malta.xml -it 15 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_15/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_15/worker.txt")


    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone16/config_before_malta.xml -it 16 -year 2009 -bkup 0")
    os.system("python /workspace/openamos/core/malta_integration/malta_dummy.py")
    os.system("python /workspace/openamos/core/openamos_run.py -file /workspace/openamos/configs/trb_2013/mag_zone16/config_after_malta.xml -it 16 -year 2009 -bkup 1")
    os.system("python /workspace/misc/stats.py")
    os.system("mv /workspace/misc/worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_16/worker.txt")
    os.system("mv /workspace/misc/non-worker.txt /workspace/projects/mag_zone_dynamic/year_2009/iteration_16/worker.txt")

