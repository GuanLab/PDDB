#!/usr/bin/perl
#
## map all records to individual;
## for each individual, let us pick up the maximal predictions


$fold=$ARGV[0];

open MAP, "../../full_train_data/Walking_activity_training.tsv" or die;
<MAP>;
while ($line=<MAP>){
	chomp $line;
	$line=~s/"//g;
	@table=split "\t", $line;
	$map{$table[2]}=$table[3];
}
close MAP;




#@mat=glob("eva.txt*train");
#$total_file=0;
$file_i=1;
while ($file_i<6){
	open PRED, "fold_${fold}/outbound/eva.txt.${file_i}.train" or die;
	open GS, "train_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref[$file_i]{$table_gs[0]}+=$table[1];
			$ref_count[$file_i]{$table_gs[0]}++;
			$pid{$table_gs[0]}=0;
		}
		$i++;
	}
	close PRED;
	$file_i++;
}

@all_record=keys %pid;
$file_i=1;
while ($file_i<6){
	foreach $record (@all_record){
		if ($ref[$file_i]{$record}>$ref_map[$file_i]{$map{$record}}){
			$ref_map[$file_i]{$map{$record}}=$ref[$file_i]{$record};
		}
	}
	$file_i++;
}

$file_i=1;
while ($file_i<6){
	foreach $record (@all_record){
		if ($ref_map[$file_i]{$map{$record}} eq ""){}else{
			$total[$file_i]+=$ref_map[$file_i]{$map{$record}};
			$total_c[$file_i]++;
		}

	}
	$file_i++;
}

$file_i=1;
while ($file_i<6){
	$avg[$file_i]=$total[$file_i]/$total_c[$file_i];
	$file_i++;
}






$file_i=1;
while ($file_i<6){
	open PRED, "fold_${fold}/rest/eva.txt.${file_i}.train" or die;
	open GS, "train_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref_rest[$file_i]{$table_gs[0]}+=$table[1];
			$ref_rest_count[$file_i]{$table_gs[0]}++;
			$pid_rest{$table_gs[0]}=0;
		}
		$i++;
	}
	close PRED;
	$file_i++;
}

@all_record_rest=keys %pid_rest;
$file_i=1;
while ($file_i<6){
	foreach $record (@all_record_rest){
		if ($ref_rest[$file_i]{$record}>$ref_map_rest[$file_i]{$map{$record}}){
			$ref_map_rest[$file_i]{$map{$record}}=$ref_rest[$file_i]{$record};
		}
	}
	$file_i++;
}

$file_i=1;
while ($file_i<6){
	foreach $record (@all_record_rest){
		if ($ref_map_rest[$file_i]{$map{$record}} eq ""){}else{
			$total_rest[$file_i]+=$ref_map_rest[$file_i]{$map{$record}};
			$total_c_rest[$file_i]++;
		}

	}
	$file_i++;
}

$file_i=1;
while ($file_i<6){
	$avg_rest[$file_i]=$total_rest[$file_i]/$total_c_rest[$file_i];
	$file_i++;
}




$file_i=1;
while ($file_i<6){
	open PRED, "fold_${fold}/return/eva.txt.${file_i}.train" or die;
	open GS, "train_gs.dat" or die;
	$i=0;
	while ($line=<PRED>){
		chomp $line;
		@table=split "\t", $line;
		$gs=<GS>;
		chomp $gs;
		@table_gs=split "\t", $gs;

		if ($table[1] eq ""){}else{
			$ref_return[$file_i]{$table_gs[0]}+=$table[1];
			$ref_return_count[$file_i]{$table_gs[0]}++;
			$pid_return{$table_gs[0]}=0;
		}
		$i++;
	}
	close PRED;
	$file_i++;
}

@all_record_return=keys %pid_return;
$file_i=1;
while ($file_i<6){
	foreach $record (@all_record_return){
		if ($ref_return[$file_i]{$record}>$ref_map_return[$file_i]{$map{$record}}){
			$ref_map_return[$file_i]{$map{$record}}=$ref_return[$file_i]{$record};
		}
	}
	$file_i++;
}

$file_i=1;
while ($file_i<6){
	foreach $record (@all_record_return){
		if ($ref_map_return[$file_i]{$map{$record}} eq ""){}else{
			$total_return[$file_i]+=$ref_map_return[$file_i]{$map{$record}};
			$total_c_return[$file_i]++;
		}

	}
	$file_i++;
}

$file_i=1;
while ($file_i<6){
	$avg_return[$file_i]=$total_return[$file_i]/$total_c_return[$file_i];
	$file_i++;
}

















open FINAL, ">feature_train.txt" or die;
open FILE, "train_gs.dat" or die;
$i=0;
while ($line=<FILE>){
	chomp $line;
	@table=split "\t", $line;
	print FINAL "$table[1]";

	$file_i=1;
	while ($file_i<6){
		if ($ref_map[$file_i]{$map{$table[0]}} eq ""){
			print FINAL "\t$avg[$file_i]";
		}else{
			$val=$ref_map[$file_i]{$map{$table[0]}};
			print FINAL "\t$val";
		}
		$file_i++;
	}


	$file_i=1;
	while ($file_i<6){
		if ($ref_map_rest[$file_i]{$map{$table[0]}} eq ""){
			print FINAL "\t$avg_rest[$file_i]";
		}else{
			$val=$ref_map_rest[$file_i]{$map{$table[0]}};
			print FINAL "\t$val";
		}
		$file_i++;
	}


	$file_i=1;
	while ($file_i<6){
		if ($ref_map_return[$file_i]{$map{$table[0]}} eq ""){
			print FINAL "\t$avg_return[$file_i]";
		}else{
			$val=$ref_map_return[$file_i]{$map{$table[0]}};
			print FINAL "\t$val";
		}
		$file_i++;
	}

	print FINAL "\n";
	$i++;
}
close FINAL;
close FILE;

