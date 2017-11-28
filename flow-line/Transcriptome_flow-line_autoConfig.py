"""
For Transcriptome Flow-line Automatic configuration 

"""
import argparse
import os
import sys
import re
import pandas as pd
bin = os.path.abspath(os.path.dirname(__file__))
sys.path.append(bin + '/../lib')
from PipMethod import myconf,generateShell,mkdir
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

__author__='Yuan Zan'
__mail__= 'seqyuan@gmail.com'
__date__= '20170728'


class readinfo:
    Genome_version = None
    ppi_species = None
    info_df = pd.DataFrame()
    de_cmp_df = pd.DataFrame()
    deg_cmp_df = pd.DataFrame()


    def __init__(self, info_file, outdir,config):
        self.info_file = info_file
        self.outdir = outdir
        self.config = config
        self.read_info()
        self.read_cmp()
        self.read_genome_version()

    def read_info(self):
        df = pd.read_excel(self.info_file, sheetname=0)
        sample_is, sample_ie = 0, 0
        for i,row in df.iterrows():
            if row[0] == "样品名称": 
                sample_is = i          
                break

        df = pd.read_excel(self.info_file, sheetname=0,header=sample_is+1)
        for i,row in df.iterrows():
            if row["样品名称"] == "差异比较组合" or pd.isnull(row["样品名称"]) or pd.isnull(row["样品编号"]) or pd.isnull(row["物种拉丁名"]) or pd.isnull(row["样品描述"]) or pd.isnull(row["结题报告中样品名称"]) or pd.isnull(row["分组"]):
                break
            sample_ie = i
        info_df = df[["样品名称","样品编号","物种拉丁名","样品描述","结题报告中样品名称","分组"]].ix[0:sample_ie,:]

        self.info_df = info_df
        #self.config.set("sample",info_df.to_string(index=False,header=False))
        for i,row in info_df.iterrows():
            self.config.set("sample",'\t'.join(row))

        sample_dup = info_df["样品名称"][info_df["样品名称"].duplicated(keep='first')]
        report_sample_dup = info_df["结题报告中样品名称"][info_df["结题报告中样品名称"].duplicated(keep='first')]
        if sample_dup.shape[0] != 0 or sample_dup.shape[0] != 0:
            if sample_dup.shape[0] != 0:
                sys.stderr.write ("以下 样品名称  有重复,请修正:\n")
                sys.stderr.write (" ".join(set(sample_dup)))
            if sample_dup.shape[0] != 0:
                sys.stderr.write ("\n以下 结题报告中样品名称  有重复,请修正:\n")
                sys.stderr.write (" ".join(set(report_sample_dup))+"\n")
            sys.exit(1)

        pipe_info = os.path.join(self.outdir,"info.txt")
        info_df.to_csv(pipe_info,sep='\t', header=None,index=None,encoding="utf-8")
        self.config.set("Para",'Para_info',pipe_info)
        sample_list_file = os.path.join(self.outdir,"sample.list")
        info_df[['结题报告中样品名称']].to_csv(sample_list_file,sep='\t', header=None,index=None,encoding="utf-8")
        self.config.set("Para",'Para_list',sample_list_file)

    def read_cmp(self):
        df = pd.read_excel(self.info_file, sheetname=0)
        cmp_is, cmp_ie = 0, 0
        for i,row in df.iterrows():
            if row[0] == "比较组合": 
                cmp_is = i          
                break

        df = pd.read_excel(self.info_file, sheetname=0,header=cmp_is+1)

        for i,row in df[["比较组合","处理组","参考组"]].iterrows():
            if pd.isnull(row["比较组合"]) or pd.isnull(row["处理组"]) or pd.isnull(row["参考组"]):
                break
            cmp_ie = i
        cmp_df = df[["比较组合","处理组","参考组"]].ix[0:cmp_ie,1:]
        deg_cmp_df = cmp_df[cmp_df['处理组'].isin(self.info_df["结题报告中样品名称"]) & cmp_df['参考组'].isin(self.info_df["结题报告中样品名称"])]
        de_cmp_df = cmp_df[~(cmp_df['处理组'].isin(self.info_df["结题报告中样品名称"]) & cmp_df['参考组'].isin(self.info_df["结题报告中样品名称"]))]

        pipe_cmp = os.path.join(self.outdir,"cmp.txt")
        cmp_df.to_csv(pipe_cmp,sep='\t', header=None,index=None,encoding="utf-8")

        self.config.set("Para",'Para_cmpFile',pipe_cmp)

        #de_cmp_df.to_csv(os.path.join(self.outdir,"de_cmp.txt"),sep='\t', header=None,index=None,encoding="utf-8")
        #deg_cmp_df.to_csv(os.path.join(self.outdir,"deg_cmp.txt"),sep='\t', header=None,index=None,encoding="utf-8")
        de_cmp_df['dedeg'] = 'deseq'
        deg_cmp_df['dedeg'] = 'degseq'
        for i,row in de_cmp_df.iterrows():
            self.config.set("cmp",'\t'.join(row))
        for i,row in deg_cmp_df.iterrows():             
            self.config.set("cmp",'\t'.join(row))
        #self.config.set("cmp",de_cmp_df.to_string(index=False,header=False,justify ='left'))
        #self.config.set("cmp",deg_cmp_df.to_string(index=False,header=False,justify ='left'))


    def read_genome_version(self):
        df = pd.read_excel(self.info_file, sheetname=0,index_col = 0)
        df = df.T
        self.Genome_version = df.ix[0,'参考基因组版本选择']
        self.config.set("Para",'Para_species',self.Genome_version)
        self.ppi_species = df.ix[0,'蛋白互作参考物种']
        self.config.set("Para",'Para_ppi_species',self.ppi_species)


class read_filter_config_feedback:
    def __init__(self, filter_config_file, feedback_file,config):
        self.sub_project_id = None
        self.finished = 'no'
        self.filter_config_file = filter_config_file
        self.feedback_file = feedback_file
        self.config = config
        self.filter_config()
        self.feedback_config()

    def filter_config(self):
        config_filter = myconf()
        config_filter.readfp(open(self.filter_config_file,encoding="utf-8"))
        self.sub_project_id = config_filter.get("CONTROL","project")
        projectName = config_filter.get("CONTROL","project_name")
        projectName = projectName.lstrip(self.sub_project_id)
        projectName = projectName.rstrip('任务单')
        projectName = projectName.rstrip('测序')
        projectName = projectName.rstrip('建库')
        projectName = projectName.rstrip('过滤')
        seq_tyep = config_filter.get("CONTROL","seq_tyep")
        SE = seq_tyep[:2]
        self.config.set("Para","Para_projectName",projectName)
        self.config.set("Para","Para_seq",seq_tyep)
        self.config.set("Para","Para_SE",SE)

    def feedback_config(self):
        config_feedback = myconf()
        config_feedback.readfp(open(self.feedback_file,encoding="utf-8"))
        try:
            self.finished = config_feedback.get("DATA","finish")
        except:
            sys.stderr.write("feedback_file is not ok!\n")
            sys.exit(1)


def default_Para(config,indir):
    [config.add_section(i) for i in ['sample','cmp','Para']]
    config.set("Para","Para_num","4")
    config.set("Para","Para_foldchange","2")
    config.set("Para","Para_pval","0.05")
    config.set("Para","Para_qval","0.05")
    config.set("Para","Para_clean",os.path.join(indir,"Filter","Filter_Result"))
    config.set("Para","Para_strand","no")
    config.set("Para","Para_lib","clean")
    config.set("Para","Para_search","gene_id")
    config.set("Para","Para_search","gene_id")
    config.set("Para","Para_feature","exon")

class generate_pipeline_qsub:
    def __init__(self, python3, pipeline_generate,pipe_type,config_file,sub_project_id,outdir,pipeline_config_file,pipelineDir):
        self.work_shell = None
        self.python3 = python3
        self.pipeline_generate = pipeline_generate
        self.pipe_type = pipe_type
        self.config_file = config_file
        self.sub_project_id = sub_project_id
        self.pipeline_config_file = pipeline_config_file
        self.pipelineDir = pipelineDir
        self.outdir = outdir
        self.generate_pipeline()
        #self.qsub_workshell()

    def generate_pipeline(self):
        work_shell = os.path.join(self.outdir,'work.sh')
        self.work_shell = work_shell
        mkdir(['{0}/Analysis'.format(self.outdir)])
        content = "{0} {1} -i {2} -o {3}/pipeline && \\\n".format(self.python3,self.pipeline_generate,self.pipeline_config_file,self.outdir)
        content += "{0} {1}/pipeline.py -i {2} -j {3} -b {4} -o {1}/Analysis -name {5} -r".format(self.python3,self.outdir,self.config_file,self.sub_project_id,self.pipelineDir,self.pipe_type)
        generateShell(work_shell,content)

    def nohup_workshell(self):
        cmd = 'cd {0} && nohup sh {1}\n'.format(self.outdir,work_shell)
        try:
            os.system(cmd)
        except:
            stderr.write("自动执行work.sh出现了一些问题,请手动执行排查\n")
            sys.exit(1)

def concession(indir):
    concession = False
    concession_conf = myconf()
    concession_file = os.path.join(indir,"concession.ini")
    if not os.path.isfile(concession_file):
        return concession

    concession_conf.readfp(open(concession_file,encoding="utf-8"))
    if concession_conf.has_section("sample") and concession_conf.has_option("sample","all_concession") and concession_conf['sample']["all_concession"]=="yes":
        return True
    else:
        return concession

def main():
    parser=argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='author:\t{0}\nmail:\t{1}\ndate:\t{2}\n'.format(__author__,__mail__,__date__))
    parser.add_argument('-in','--indir',help='which dir have Filter info Analysis concession',dest='indir',type=str,default=os.path.abspath(os.getcwd()))
    parser.add_argument('-t','--type',help='pipeline type',dest='type',type=str,required=True)   
    parser.add_argument('-c','--category',help='species category',dest='category',type=str,default=os.path.join(bin,'species_category.ini'))
    parser.add_argument('-cf','--pipeline_config',help='pipeline_config.ini',dest='pipeline_config',type=str,default=os.path.join(bin,'config_pipeline.ini'))
    parser.add_argument('-py','--python3',help='python3 path',dest='python3',type=str,default='/annoroad/share/software/install/Python-3.3.2/bin/python3')
    parser.add_argument('-pg','--pipeline_generate',help='path of pipeline_generate.py',dest='pipeline_generate',type=str,default='/annoroad/bioinfo/PMO/liutao/pipeline_generate/bin/current/pipeline_generate.py')
    parser.add_argument('-pipd','--pipelineDir',help='pipeline_bin',dest='pipelineDir',type=str,default='/annoroad/data1/bioinfo/PROJECT/RD/Cooperation/RNA/LncRNA/ngs_bioinfo/TET-402/liujunwu/Analysis/GIT/Transcriptome_pipeline/bin')


    args=parser.parse_args()

    config = myconf()
    config_category = myconf()
    config_category.readfp(open(args.category,encoding="utf-8"))
    "判断输出目录是否建立"
    if not os.path.isdir(args.indir):
        sys.stderr.write("Your dir is not make!\n{0}\n".format(args.indir))
        sys.exit(1)

    outdir = os.path.join(args.indir,"Analysis-test")
    config_file = os.path.join(outdir,"config.ini")
    Path(config_file).touch()
    Path(config_file).unlink()
    #Path(config_file).touch()
    #config.readfp(open(config_file,encoding="utf-8"))

    "设置默认参数"
    default_Para(config,args.indir)

    "设置从过滤目录获得的参数"
    feedback_file = os.path.join(args.indir,"Filter","Filter_Result","email","email_feedback.txt")
    filter_config_file = os.path.join(args.indir,"Filter","Filter_Result","config.ini")

    if not os.path.isfile(feedback_file) or not os.path.isfile(filter_config_file):
        sys.stderr.write("filter is not ok\n")
        sys.exit(1)

    filter_feedback = read_filter_config_feedback(filter_config_file,feedback_file,config)

    "设置从subproject_info.xls获得的参数"
    subprojectID_info_file = os.path.join(args.indir,'info',"{0}_info.xls".format(filter_feedback.sub_project_id))
    subprojectID_info_file2 = os.path.join(args.indir,'info',"{0}_info.xlsx".format(filter_feedback.sub_project_id))

    if os.path.isfile(subprojectID_info_file):
        pass
    elif os.path.isfile(subprojectID_info_file2):
        subprojectID_info_file = subprojectID_info_file2
    else:
        sys.stderr.write("信息搜集表还没准备好,请及时上传\n")
        sys.exit(1)

    info = readinfo(subprojectID_info_file,outdir,config)

    config.set("Para","Para_ProjectType",args.type)
    config.set("Para","Para_project","{0}_{1}".format(args.type,filter_feedback.sub_project_id))
    config.set("Para","Para_category",config_category.get("category",info.Genome_version))
    config.write(open(config_file, "w+")) 

    config_pipeline = myconf()
    config_category.readfp(open(args.pipeline_config,encoding="utf-8"))
    config_pipeline_file = config_category.get('config',args.type)

    pip_qsub = generate_pipeline_qsub(args.python3, args.pipeline_generate,args.type,config_file,filter_feedback.sub_project_id,outdir,config_pipeline_file,args.pipelineDir)

    if filter_feedback.finished == "yes" or concession(args.indir):
        #pip_qsub.nohup_workshell()
        pass
        sys.stdout.write('成功投递任务\n')


if __name__=="__main__": 
    main()