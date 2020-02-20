#!/bin/bash

for i in 0 1 2 3 4
do
    perl split_gold_standard_by_record.pl ${i}

    perl prepare_accel_walking_outbound_train.pl
    perl prepare_accel_walking_outbound_test.pl
    python train.py accl_outbound_train.txt 4000 guan_version1_4000

    cp fold1_params_100 params
    python predict.py accl_outbound_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.1.test
    python predict.py full_accl_outbound_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.1.train

    cp fold2_params_100 params
    python predict.py accl_outbound_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.2.test
    python predict.py full_accl_outbound_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.2.train

    cp fold3_params_100 params
    python predict.py accl_outbound_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.3.test
    python predict.py full_accl_outbound_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.3.train

    cp fold4_params_100 params
    python predict.py accl_outbound_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.4.test
    python predict.py full_accl_outbound_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.4.train

    cp fold5_params_100 params
    python predict.py accl_outbound_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.5.test
    python predict.py full_accl_outbound_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.5.train

    mkdir fold_${i}
    mkdir fold_${i}/outbound
    mv fold*params* fold_${i}/outbound/
    mv eva.txt* fold_${i}/outbound/
    mv accl_*txt fold_${i}/outbound/
    mv training_loss.txt fold_${i}/outbound/training_loss_outbound.txt

    perl prepare_accel_walking_rest_train.pl
    perl prepare_accel_walking_rest_test.pl
    python train.py accl_rest_train.txt 4000 guan_version1_4000

    cp fold1_params_100 params
    python predict.py accl_rest_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.1.test
    python predict.py full_accl_rest_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.1.train

    cp fold2_params_100 params
    python predict.py accl_rest_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.2.test
    python predict.py full_accl_rest_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.2.train

    cp fold3_params_100 params
    python predict.py accl_rest_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.3.test
    python predict.py full_accl_rest_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.3.train

    cp fold4_params_100 params
    python predict.py accl_rest_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.4.test
    python predict.py full_accl_rest_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.4.train

    cp fold5_params_100 params
    python predict.py accl_rest_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.5.test
    python predict.py full_accl_rest_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.5.train



    mkdir fold_${i}/rest
    mv fold*params* fold_${i}/rest/
    mv eva.txt* fold_${i}/rest/
    mv accl_*txt fold_${i}/rest/
    mv training_loss.txt fold_${i}/rest/training_loss_rest.txt




    perl prepare_accel_walking_return_train.pl
    perl prepare_accel_walking_return_test.pl
    python train.py accl_return_train.txt 4000 guan_version1_4000

    cp fold1_params_100 params
    python predict.py accl_return_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.1.test
    python predict.py full_accl_return_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.1.train

    cp fold2_params_100 params
    python predict.py accl_return_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.2.test
    python predict.py full_accl_return_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.2.train

    cp fold3_params_100 params
    python predict.py accl_return_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.3.test
    python predict.py full_accl_return_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.3.train

    cp fold4_params_100 params
    python predict.py accl_return_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.4.test
    python predict.py full_accl_return_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.4.train

    cp fold5_params_100 params
    python predict.py accl_return_test.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.5.test
    python predict.py full_accl_return_train.txt 4000 guan_version1_4000
    cp eva.txt eva.txt.5.train



    mkdir fold_${i}/return
    mv fold*params* fold_${i}/return
    mv eva.txt* fold_${i}/return/
    mv accl_*txt fold_${i}/return/
    mv training_loss.txt fold_${i}/return/training_loss_return.txt

    perl pull_dl_prediction_test.pl ${i}
    perl pull_dl_prediction_train.pl ${i}
    python prediction.py
    python evaluation.py
    cp auc.txt ${i}.auc.txt

    perl pull_dl_prediction_test_5sep.pl ${i}
    perl pull_dl_prediction_train_5sep.pl ${i}
    python prediction.py
    python evaluation.py
    cp auc.txt ${i}.5sep.auc.txt


    perl pull_dl_prediction_by_individual_test.pl ${i}
    perl pull_dl_prediction_by_individual_train.pl ${i}
    python prediction.py
    python evaluation.py
    cp auc.txt ${i}.ind.auc.txt


    perl pull_dl_prediction_by_individual_test_5sep.pl ${i}
    perl pull_dl_prediction_by_individual_train_5sep.pl ${i}
    python prediction.py
    python evaluation.py
    cp auc.txt ${i}.ind.5sep.auc.txt

    perl pull_dl_prediction_by_individual_max_test.pl ${i}
    perl pull_dl_prediction_by_individual_max_train.pl ${i}
    python prediction.py
    python evaluation.py
    cp auc.txt ${i}.ind.max.auc.txt


    perl pull_dl_prediction_by_individual_max_test.pl ${i}
    perl pull_dl_prediction_by_individual_max_train.pl ${i}
    python prediction.py
    python evaluation.py
    cp auc.txt ${i}.ind.max.auc.txt


    perl pull_dl_prediction_by_individual_max_test_5sep.pl ${i}
    perl pull_dl_prediction_by_individual_max_train_5sep.pl ${i}
    python prediction.py
    python evaluation.py
    cp auc.txt ${i}.ind.max.5sep.auc.txt


    mv  *auc* fold_${i}/

done
