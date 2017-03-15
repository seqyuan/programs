package main

import (
//    "errors"
	"flag"
	"bufio"
	"bytes"
	"database/sql"
	"fmt"
	"github.com/dgiagio/getpass"
	_ "github.com/mattn/go-sqlite3"
	"github.com/tealeg/xlsx"
	"log"
	"os"
	"os/exec"
	"os/user"
	"path/filepath"
	"regexp"
	"strconv"
	"strings"
	"time"
)


/*
type error interface {
    Error() string
}

func (cerr Customerror) Error() string {
    errorinfo := fmt.Sprintf("infoa : %s , infob : %s , original err info : %s ", cerr.infoa, cerr.infob, cerr.Err.Error())
    return errorinfo
}
*/
func usage() {
	fmt.Printf("\nProgram: applyProject (Tools for apply project)\nVersion: 0.1.1-20170214\n注意输入不能有中文标点符号!\nXshell删除字符时请按住Ctrl键\n\nUsage:\tapplyProject <command> [options]\n\n")
	fmt.Printf("Command:\n")
	fmt.Printf("    a|apply                 Apply a project\n")
	fmt.Printf("    q|query                 Query the apply projects of your groups\n")
	fmt.Printf("    e|edit [id]             ReEdit the apply project\n")
	fmt.Printf("    d|delete [id]           Delete the apply project\n\n")

	fmt.Printf("   eu|editusr               ReEdit usr information\n")
	fmt.Printf("    o|outDir [dir]          Dir to export apply projects excel file(then you can send it by email)\n")
	fmt.Printf("    m|mail [out.xlsx]       Send the Excel to taoliu@genome.cn\n\n")

	fmt.Printf("    -flagplus               This week last week flag change\n")
	fmt.Printf("    -creatdb                Reset applyProject DB only for admin\n")
	fmt.Printf("    -creatusrdb             Reset usr DB only for admin\n")
	fmt.Printf("    -importOldxls [xlsFile] Import old projects from excel only for admin\n\n")
	
}

func checkErr(err error) {
	//logger := log.New(os.Stdio, "\n",\t log.Ldate|log.Ltime|log.Llongfile)
	//var mylog = log.New(os.Stderr, "app: ", log.LstdFlags|log.Lshortfile)
	if err != nil {
		//panic(err)
		log.Fatal(err)
	}
}
func myinput(content string) (result string) {
	inputReader := bufio.NewReader(os.Stdin)
	for result == "" {
		fmt.Println("\n>>>", content)
		input, err := inputReader.ReadString('\n')
		input = strings.Replace(input, "\n", "", -1)
		if err != nil {
			fmt.Println("There ware errors reading, input again\n")
			continue
		}
		if input == "exit" {
			os.Exit(1)
		}
		result = input
		//fmt.Printf("Your input is %s", input)
	}
	return result
}

func myinput_compatibleEmpty(content string) (result string) {
	inputReader := bufio.NewReader(os.Stdin)
	//var err error = errors.New("this is a new error")

	for {
		fmt.Println("\n>>>", content)
		input, err := inputReader.ReadString('\n')
		input = strings.Replace(input, "\n", "", -1)
		if err != nil {
			fmt.Println("There ware errors reading, input again\n")
			continue
		}
		if input == "exit" {
			os.Exit(1)
		}
		result = input
		break
		//fmt.Printf("Your input is %s", input)
	}
	return result
}

func exportExcel(db *sql.DB, usr string, outDir string) {
	defer db.Close()
	var (
		xlsxFile *xlsx.File
		sheet    *xlsx.Sheet
		//	row *xlsx.Row
		//	cell *xlsx.Cell
		err error
	)
	var (
//		id                int
//		user              string
		name              string
		groups            string
//		project_type      string
		project_name      string
		start_time        string
		end_time          string
		project_txt       string
		pre_target        string
		complete_standard string
		need_time         string
//		flag              int
		project_stat      string
//		sub_project_ID    string
	)

	row := db.QueryRow("select groups from usrInfo where user = ?", usr)
	err = row.Scan(&groups)

	xlsxFile = xlsx.NewFile()
	fileName := fmt.Sprintf("%s_下单申请", groups)
	sheet1 := fmt.Sprintf("本周立项申请")
	sheet, _ = xlsxFile.AddSheet(sheet1)

	rows, err := db.Query("select project_name, name, start_time, end_time, project_txt,pre_target,complete_standard,need_time from applyProject where groups = ? and flag = 0 order by user", groups)
	defer rows.Close()
	if err != nil {
		fmt.Println("你们组没有要申请的项目！")
		defer rows.Close()
		os.Exit(1)
	}

	slice := []string{"任务单名称", "信息负责人", "信息起始日期", "信息截止日期", "分析内容","预期目标","完成标准", "估时"}
	xlsrow := sheet.AddRow()
	for _, value := range slice {
		cell := xlsrow.AddCell()

		style := cell.GetStyle()
		style.Border.Top = "thin"
		style.Border.Bottom = "thin"
		style.Border.Left = "thin"
		style.Border.Right = "thin"
		style.ApplyBorder = true

		cell.Value = value
	}

	//ids := make([]int, 100)
	//i := 0
	for rows.Next() {
		err = rows.Scan(&project_name,&name, &start_time, &end_time, &project_txt, &pre_target,&complete_standard,&need_time)
		//ids[i] = id
		//i = i + 1

		checkErr(err)
		xlsrow = sheet.AddRow()
		slice := []string{project_name, name, start_time, end_time, project_txt,pre_target,complete_standard,need_time}
		for _, value := range slice {
			cell := xlsrow.AddCell()

			style := cell.GetStyle()
			style.Border.Top = "thin"
			style.Border.Bottom = "thin"
			style.Border.Left = "thin"
			style.Border.Right = "thin"
			style.ApplyBorder = true

			cell.Value = value
		}
	}

	//sheet2  上周项目完成情况/////////////////////////////////////////////////////////////////////////////////////////////////////
	sheet2 := fmt.Sprintf("上周项目完成情况")
	sheet, _ = xlsxFile.AddSheet(sheet2)

	rows2, err := db.Query("select project_name, name, start_time, end_time, project_txt,need_time,project_stat from applyProject where groups = ? and flag = 1 order by user", groups)
	defer rows2.Close()
	if err != nil {
		fmt.Println("你们组上周没有申请项目--请联系程序管理员更新项目flag状态！")
		defer rows2.Close()
		os.Exit(1)
	}
	slice2 := []string{"任务单名称", "信息负责人", "信息起始日期", "信息截止日期", "分析内容","估时","完成情况"}
	xlsrow2 := sheet.AddRow()
	for _, value := range slice2 {
		cell := xlsrow2.AddCell()

		style := cell.GetStyle()
		style.Border.Top = "thin"
		style.Border.Bottom = "thin"
		style.Border.Left = "thin"
		style.Border.Right = "thin"
		style.ApplyBorder = true

		cell.Value = value
	}

	//ids = make([]int, 100)
	//i = 0
	for rows2.Next() {
		err = rows2.Scan(&project_name, &name, &start_time, &end_time, &project_txt,&need_time,&project_stat)
		//fmt.Println(id)
		//ids[i] = id
		//i = i + 1

		checkErr(err)
		xlsrow2 = sheet.AddRow()
		slice := []string{project_name, name, start_time, end_time, project_txt,need_time,project_stat}
		for _, value := range slice {
			cell := xlsrow2.AddCell()

			style := cell.GetStyle()
			style.Border.Top = "thin"
			style.Border.Bottom = "thin"
			style.Border.Left = "thin"
			style.Border.Right = "thin"
			style.ApplyBorder = true

			cell.Value = value
		}
	}
	//sheet2 ^^^^上周项目完成情况^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

	t := time.Now()
	/*fmt.Printf("%d-%02d-%02dT%02d:%02d:%02d-00:00\n",
	  t.Year(), t.Month(), t.Day(),
	  t.Hour(), t.Minute(), t.Second())
	*/
	outExcel := fmt.Sprintf("%s/%s_%d-%02d-%02dT%02d-%02d.xlsx", outDir, fileName, t.Year(), t.Month(), t.Day(), t.Hour(), t.Minute())
	err = xlsxFile.Save(outExcel)
	if err != nil {
		fmt.Printf("save xlsx file fail , error : %s", err.Error())
		fmt.Printf("提供一个可写的目录以供输出excel")
		//return
	}
	//	defer rows.Close()
	/*
	for _, value := range ids[:i] {
		stmt, err := db.Prepare("delete from applyProject where id=?")
		checkErr(err)
		_, err = stmt.Exec(value)
		checkErr(err)
	}
	*/
	os.Exit(1)
}

func Sendmail(db *sql.DB, usr string, xlsxfile string, bin string) {
	var email string
	row := db.QueryRow("select email from usrInfo where user = ?", usr)
	err := row.Scan(&email)
	checkErr(err)
	defer db.Close()

	in := bytes.NewBuffer(nil)
	cmd := exec.Command("sh")
	cmd.Stdin = in
	var out bytes.Buffer
	cmd.Stdout = &out

	pass, _ := getpass.GetPassword(fmt.Sprintf("Please input password of %s: ", email))

	fmt.Println("sending...")
	go func() {
		cmdString := fmt.Sprintf("ssh c0008 2> /dev/null \"/annoroad/share/software/install/Python-3.3.2/bin/python3 %s/sendEmail.py %s %s\"", bin, pass, xlsxfile)
		//fmt.Println(cmdString)
		in.WriteString(cmdString)
		//in.WriteString("exit\n")
	}()
	err = cmd.Run()
	fmt.Printf(out.String())

	if err != nil {
		fmt.Println(err)
		//return
		//os.Exit(1)
	}
}

func Printrows(rows *sql.Rows) {
	fmt.Println("\nid\t信息负责人\t任务单名称\t起始时间\t结束时间\t分析内容\t预期目标\t完成标准\t估时")
	var (
		id                int
//		user              string
		name              string
//		groups            string
//		project_type      string
		project_name      string
		start_time        string
		end_time          string
		project_txt       string
		Pre_target        string
		Complete_standard string
		need_time         string
	)
	for rows.Next() {
		err := rows.Scan(&id, &name, &project_name, &start_time, &end_time, &project_txt,&Pre_target, &Complete_standard, &need_time)
		checkErr(err)
		//fmt.Printf("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", id, user, name, groups, project_type, project_name, start_time, end_time, project_txt, need_time)
		fmt.Printf("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", id, name, project_name, start_time, end_time, project_txt,Pre_target,Complete_standard, need_time)
	}
	fmt.Println("\n")
}

func PrintUsrInforows(rows *sql.Rows) {
	fmt.Println("人员信息列表")
	fmt.Println("id\t集群账号\t姓名\t组别\t邮箱")
	var (
		id     int
		user   string
		name   string
		groups string
		email  string
	)
	for rows.Next() {
		err := rows.Scan(&id, &user, &name, &groups, &email)
		checkErr(err)
		fmt.Printf("%d\t%s\t%s\t%s\t%s", id, user, name, groups, email)
	}
}

func CreatDB(db *sql.DB) {
	defer db.Close()
	drp_tb_sql := "drop table if exists applyProject"
	_, err := db.Exec(drp_tb_sql)
	sqlStmt := `
	create table if not exists applyProject (
		id integer unique not null primary key,
		user string,
		name string,
		groups string,
		project_name string unique not null,
		start_time string,
		end_time string,
		project_txt string,
		Pre_target string,
		Complete_standard string,
		need_time string,
		flag int,
		project_stat string,
		sub_project_ID string
		);
		`
		//flag 0 this week,1 last week ,2 at least 2 two weeks ago
	_, err = db.Exec(sqlStmt)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
//		return
	}
	//usr, _ := user.Current()
	//QueryDB(db, usr.Username)
	os.Exit(1)
}

func QueryDB(db *sql.DB, usr string) {
	//查询所在组申请项目
	defer db.Close()
	var groups string
	row := db.QueryRow("select groups from usrInfo where user = ?", usr)
	err := row.Scan(&groups)

	rows, err := db.Query("select id, name, project_name, start_time, end_time, project_txt,Pre_target,Complete_standard, need_time from applyProject where groups = ? and flag = 0 order by user", groups)
	defer rows.Close()
	if err == nil {
		Printrows(rows)
	}
	os.Exit(1)
}

func CreatUsrInfoDB(db *sql.DB) {
	defer db.Close()
	drp_tb_sql := "drop table if exists usrInfo"
	_, err := db.Exec(drp_tb_sql)
	sqlStmt := `
	create table if not exists usrInfo (
		id integer unique not null primary key,
		user string unique not null,
		name string,
		groups string,
		email string
		);
		`
	_, err = db.Exec(sqlStmt)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
//		return
	}
	//QueryUsrInfoDB(db)
	os.Exit(1)
}
func QueryUsrInfoDB(db *sql.DB) {
	//查询数据
	rows, err := db.Query("select * from usrInfo order by groups")
	checkErr(err)
	defer rows.Close()
	PrintUsrInforows(rows)
	defer rows.Close()
}

func checkUsrInfoDB(db *sql.DB, usr string) {
//	defer db.Close()
	//检查信息用户信息
	var (
		id     int
		user   string
		name   string
		groups string
		email  string
	)
	row := db.QueryRow("select * from usrInfo where user = ?", usr)
	err := row.Scan(&id, &user, &name, &groups, &email)
	//fmt.Println(name, groups, email)
	if err != nil {
		fmt.Println("你的需要输入 姓名组别邮箱 等信息才能使用这个程序！")
		insertUsrInfoDB(db, usr)
	}
	if name == "-" || groups == "-" || email == "-" {
		fmt.Println("你需要补全 姓名组别邮箱信息 才能使用这个程序！")
		updateUsrInfoDB(db, usr)
	}
	//fmt.Println(name, groups, email)
}

func flagPlus(db *sql.DB, usr string){
	var (
		id                int
		groups            string
		flags              int
	)
	row := db.QueryRow("select groups from usrInfo where user = ?", usr)
	err := row.Scan(&groups)

	rows, err := db.Query("select id,flag from applyProject where groups = ? and flag < 2 order by id", groups)
	checkErr(err)

	m := make(map[int]int)

	defer rows.Close()
	for rows.Next() {
		err := rows.Scan(&id, &flags)
		checkErr(err)
		flags += 1
		m[id] = flags
	}

	for key, value := range m {
		stmt, err := db.Prepare("update applyProject set flag=? where id=?")
		checkErr(err)
		_, err = stmt.Exec(value, key)
		checkErr(err)
	}
	os.Exit(1)
}


type projectid struct {
    pi_project_name   string
    pi_project_stat   string
    pi_sub_project_ID string
}
//type Words map[int]projectid



func check_project_stat(db *sql.DB, usr string){
	var (
		id                int
		project_name      string
		project_stat      string
		sub_project_ID    string
	)
	rows, err := db.Query("select id,project_name,project_stat,sub_project_ID from applyProject where user = ? and flag = 1 order by id", usr)
	checkErr(err)
	defer rows.Close()
	Words := make(map[int]projectid)
	//w := make(Words)
	//m := make(map[int]string)
	for rows.Next() {
		err := rows.Scan(&id, &project_name, &project_stat, &sub_project_ID)
		checkErr(err)
		if sub_project_ID == "-" || project_stat == "-"{
			//m[id] = project_name
			Words[id]=projectid{pi_project_stat:project_stat,pi_sub_project_ID:sub_project_ID,pi_project_name:project_name}
		}
	}
	if len(Words) == 0{return}
//	fmt.Println(Words)
//	rows.Close()

	for key, value := range Words {
//		row := db.QueryRow("select sub_project_ID,project_stat from applyProject where id = ?", key)
//		err = row.Scan(&sub_project_ID, &project_stat)

		stmt, err := db.Prepare("update applyProject set project_stat=?, sub_project_ID=? where id=?")
		checkErr(err)
		fmt.Printf("\n%s\n\n此项目为上周项目有两项内容需要填写",value.pi_project_name)

		if value.pi_sub_project_ID == "-" {
			sub_project_ID = myinput("请输入此项目的子项目编号:")
		}
		if value.pi_project_stat == "-" {
			project_stat = myinput("请输入此项目的完成情况:")
		}
		//fmt.Println(sub_project_ID,project_stat)
		_, err = stmt.Exec(project_stat, sub_project_ID,key)
		checkErr(err)
/*
		affect, err := res.RowsAffected()
    	checkErr(err)
    	fmt.Println(affect)
    	*/
	}
	os.Exit(1)
}

func insertUsrInfoDB(db *sql.DB, usr string) {
	defer db.Close()
	//插入数据
	var (
		name   string
		groups string
		email  string
	)
	//row := db.QueryRow("select * from usrInfo where usr = ?", usr)
	//err := row.Scan(&id, &name, &groups, &email)

	name = myinput("请输入你的姓名:")
	groupss := map[string]string{
		"0": "转录调控组",
		"1": "生物学DNA组",
		"2": "医口DNA组",
		"3": "分析组",
	}
	for groups == "" {
		i := myinput("请输入你的组别:\n转录调控组 [0]\n生物学DNA组 [1]\n医口DNA组 [2]\n分析组 [3]\n\n如果你的组不在列表里请直接输入组名")
		groupsss, err := groupss[i]
		if err != true {
			groups = i
			fmt.Println("你输入了一个新的组名")
		} else {
			groups = groupsss
		}
	}
	for email == "" {
		email = myinput("请输入你的邮箱:")
		match, _ := regexp.MatchString("@genome.cn", email)
		if match == false {
			email = ""
		}
	}

	stmt, err := db.Prepare("insert into usrInfo(user,name,groups,email) values(?,?,?,?)")
	checkErr(err)
	_, err = stmt.Exec(usr, name, groups, email)
	checkErr(err)
	//	id, err := res.LastInsertId()
	//	checkErr(err)
	//	fmt.Println(id)
	os.Exit(1)
}

func updateUsrInfoDB(db *sql.DB, usr string) {
    defer db.Close()
	//更新数据
	var (
		id     int
		user   string
		name   string
		groups string
		email  string
	)
	row := db.QueryRow("select * from usrInfo where user = ?", usr)
	err := row.Scan(&id, &user, &name, &groups, &email)
	//fmt.Println(name, groups, email)

	name_new := myinput_compatibleEmpty(fmt.Sprintf("请输入你的姓名:%s", name))
	if name_new == "" {
		name_new = name
	}
	
	groupss := map[string]string{
			"0": "转录调控组",
			"1": "生物学DNA组",
			"2": "医口DNA组",
			"3": "分析组",
	}

    i := myinput_compatibleEmpty(fmt.Sprintf("请输入你的组别 %s\n:\n转录调控组 [0]\n生物学DNA组 [1]\n医口DNA组 [2]\n分析组 [3]\n\n如果你的组不在列表里请直接输入组名",groups))
//	if groups_new == "" {
//		groups_new = groups
//	}
    var groups_new string
    if i != "" {
        groupsss, err := groupss[i]
        if err != true {
            groups_new = i
            fmt.Println("你输入了一个新的组名")
        } else {
            groups_new = groupsss
        }
    } else {
        groups_new = groups
    }

    var email_new string
    for {
        email_new = myinput_compatibleEmpty(fmt.Sprintf("请输入你的邮箱:%s", email))
        if email_new == "" {
            email_new = email
            break
        } else {
            match, _ := regexp.MatchString("@genome.cn", email_new)
            if match == false {
                fmt.Println("请输入一个正确的以@genome.cn结尾的邮箱地址")
                continue
            }
        }
        break
    }

	stmt, err := db.Prepare("update usrInfo set name=?, groups=?, email=? where user=?")
	checkErr(err)
	_, err = stmt.Exec(name_new, groups_new, email_new, usr)
	checkErr(err)
	os.Exit(1)
}

func DeleteDB(db *sql.DB, delId int, linuxUser string) {
	//查询数据
	stmt, err := db.Prepare("select user from applyProject where id=?")
	var user string
	err = stmt.QueryRow(delId).Scan(&user)
	checkErr(err)

	if linuxUser == user {
		stmt, err = db.Prepare("delete from applyProject where id=?")
		checkErr(err)
		_, err = stmt.Exec(delId)
		//res, err := stmt.Exec(delId)
		//affect, err := res.RowsAffected()
		checkErr(err)
		//fmt.Println(affect)
	} else {
		fmt.Println("你不是这个任务单的申请人,不能对这个任务单进行操作！")
	}
	defer db.Close()
	os.Exit(1)
}

func insertDB(db *sql.DB, usr string) {
	//插入数据
	var (
		name              string
		groups            string
//		project_type      string
		project_name      string
		start_time        string
		end_time          string
		project_txt       string
		Pre_target        string
		Complete_standard string
		need_time         string
		flag              int         // 0 this week,1 last week ,2 at least 2 two weeks ago
		project_stat      string = "-"
		sub_project_id    string = "-"
	)
	row := db.QueryRow("select name, groups from usrInfo where user = ?", usr)
	err := row.Scan(&name, &groups)

	project_name = myinput("任务单名称:")
	now := time.Now()
	start_time_default := now.Format("2006/01/02")
	start_time = myinput_compatibleEmpty(fmt.Sprintf("信息起始日期(格式: %s): %s", start_time_default, start_time_default))
	if start_time == ""{
	  start_time = start_time_default
	}
	dd, _ := time.ParseDuration("24h")
  end_time_default := now.Add(6 * dd).Format("2006/01/02")
	end_time = myinput_compatibleEmpty(fmt.Sprintf("信息截止日期(格式: %s): %s", end_time_default, end_time_default))
	if end_time == ""{
	  end_time = end_time_default
	}
	project_txt = myinput("分析内容:")
	Pre_target = myinput("预期目标:")
	Complete_standard = myinput("完成标准:")
    need_time = myinput("估时(单位h,只能输入整数):")

	need_time = fmt.Sprintf("%s", strings.Trim(need_time, "h"))
	stmt, err := db.Prepare("insert into applyProject(user,name,groups,project_name,start_time,end_time, project_txt,Pre_target,Complete_standard,need_time,flag,project_stat,sub_project_id) values(?,?,?,?,?,?,?,?,?,?,?,?,?)")
	checkErr(err)
	res, err := stmt.Exec(usr, name, groups, project_name, start_time, end_time, project_txt,Pre_target,Complete_standard, need_time,flag,project_stat,sub_project_id)
	checkErr(err)
	_, err = res.LastInsertId()
	checkErr(err)
	defer db.Close()
}

func updateDB(db *sql.DB, id int, linuxUser string) {
	defer db.Close()
	//更新数据
	//fmt.Println("id", "集群账号", "姓名", "组别", "项目类别", "任务单名称", "起始时间", "结束时间", "分析内容", "估时")
	var (
		user                  string
		name                  string
//		groups                string
//		project_type          string
		project_name          string
		start_time            string
		end_time              string
		project_txt           string
		Pre_target            string
		Complete_standard     string
		need_time             string
	)

	stmt, err := db.Prepare("select user from applyProject where id=?")
	err = stmt.QueryRow(id).Scan(&user)
//	fmt.Println("qwer")
	if err != nil {
		fmt.Println("这个任务单不存在, 如果要修改请输入一个正确的任务单！")
//		defer db.Close()
		os.Exit(1)
	}

	if linuxUser != user {
		fmt.Println("你不是这个任务单的申请人,不能对这个任务单进行操作！")
//		defer db.Close()
		os.Exit(1)
	}

	//stmt, err = db.Prepare("select * from applyProject where id=?")
	//err = stmt.QueryRow(id).Scan(&id, &user, &name, &groups, &project_name, &start_time, &end_time, &project_txt,&Pre_target,&Complete_standard, &need_time)
	stmt, err = db.Prepare("select name,project_name,start_time,end_time,project_txt,Pre_target,Complete_standard,need_time from applyProject where id=?")
	err = stmt.QueryRow(id).Scan(&name, &project_name, &start_time, &end_time, &project_txt,&Pre_target,&Complete_standard, &need_time)
	
	//rows := db.QueryRow("select * from usrInfo where id = ?", id)
	//err = rows.Scan(&id, &user, &name, &groups, &project_type, &project_name, &start_time, &end_time, &project_txt, &need_time)
	checkErr(err)

	project_name_new := myinput_compatibleEmpty(fmt.Sprintf("任务单名称: %s", project_name))
	if project_name_new == "" {
		project_name_new = project_name
	}

  now := time.Now()
	start_time_default := now.Format("2006/01/02")
	
	start_time_new := myinput_compatibleEmpty(fmt.Sprintf("信息起始日期(格式: %s): %s", start_time_default, start_time))
	if start_time_new == "" {
		start_time_new = start_time
	}

  dd, _ := time.ParseDuration("24h")
  end_time_default := now.Add(6 * dd).Format("2006/01/02")
	end_time_new := myinput_compatibleEmpty(fmt.Sprintf("信息截止日期(格式: %s): %s", end_time_default, end_time))
	if end_time_new == "" {
		end_time_new = end_time
	}

	project_txt_new := myinput_compatibleEmpty(fmt.Sprintf("分析内容: %s", project_txt))
	if project_txt_new == "" {
		project_txt_new = project_txt
	}

	Pre_target_new := myinput_compatibleEmpty(fmt.Sprintf("预定目标: %s", Pre_target))
	if Pre_target_new == "" {
		Pre_target_new = Pre_target
	}

	Complete_standard_new := myinput_compatibleEmpty(fmt.Sprintf("完成标准: %s", Complete_standard))
	if Complete_standard_new == "" {
		Complete_standard_new = Complete_standard
	}

	need_time_new := myinput_compatibleEmpty(fmt.Sprintf("估时: %s", need_time))
	if need_time_new == "" {
		need_time_new = need_time
	}

	stmt, err = db.Prepare("update applyProject set project_name=?, start_time=?, end_time=?, project_txt=?, Pre_target=?, Complete_standard=?, need_time=? where id =?")
	checkErr(err)
	_, err = stmt.Exec(project_name_new, start_time_new, end_time_new, project_txt_new,Pre_target_new, Complete_standard_new, need_time_new, id)
	checkErr(err)
	os.Exit(1)
}

func importOldxls(db *sql.DB, excelFileName string){
    var (
        usr               string
        name              string
        groups            string
        project_name      string
        start_time        string
        end_time          string
        project_txt       string
        Pre_target        string
        Complete_standard string
        need_time         string
        flags              int = 0
    )
    defer db.Close()
    xlFile, err := xlsx.OpenFile(excelFileName)
	if err != nil {
        fmt.Println("open xls err")
    }

    sheet := xlFile.Sheets[0]

    for i, row := range sheet.Rows {
        if i == 0 {continue}
        stmt, err := db.Prepare("insert into applyProject(user,name,groups,project_name,start_time,end_time, project_txt,Pre_target,Complete_standard,need_time,flag,project_stat,sub_project_ID) values(?,?,?,?,?,?,?,?,?,?,?,?,?)")
        checkErr(err)
        for ii, cell := range row.Cells {
            text, _ := cell.String()
            switch ii{
            case 0:
                project_name = text
            case 1:
                name = text
                rowu := db.QueryRow("select groups from usrInfo where name = ?", name)
                err = rowu.Scan(&groups)
                fmt.Println(groups)
                checkErr(err)
                rowu = db.QueryRow("select user from usrInfo where name = ?", name)
                err = rowu.Scan(&usr)
                fmt.Println(usr)
                checkErr(err)
            case 2:
                start_time = text
            case 3:
                end_time = text
            case 4:
                project_txt = text
            case 5:
                Pre_target = text
            case 6:
                Complete_standard = text
            case 7:
                need_time = text
            }
        }
        _, err = stmt.Exec(usr, name, groups, project_name, start_time, end_time, project_txt,Pre_target,Complete_standard, need_time,flags,"-","-")
        checkErr(err)
        //_, err = res.LastInsertId()
        //checkErr(err)
    }
    os.Exit(1)
}



func main() {
	flagplus := flag.Bool("flagplus", false, "flag + 1")
	creatdb := flag.Bool("creatdb", false, "reset db")
	creatusrdb := flag.Bool("creatusrdb", false, "reset surdb")
	excelFilePath := flag.String("importOldxls", "", "excelFilePath")
	flag.Parse()
	admin := "yuanzan"
	file, _ := exec.LookPath(os.Args[0])
	filepaths, _ := filepath.Abs(file)
	bin := filepath.Dir(filepaths)

	DBfile := bin + "/tmp/applyProject.db"
	db, err := sql.Open("sqlite3", DBfile)
	checkErr(err)
	defer db.Close()
	usr, _ := user.Current()

	if *excelFilePath != ""{
		if usr.Username == admin{
			importOldxls(db,*excelFilePath)
		} else {
			fmt.Println("you are not admin, can not use -importOldxls")
			os.Exit(1)
		}
	}

	if *creatusrdb == true{
		if usr.Username == admin{
			CreatUsrInfoDB(db)
		} else {
			fmt.Println("you are not admin, can not use -creatusrdb")
			os.Exit(1)
		}
	}
	if *creatdb == true{
		if usr.Username == admin{
			CreatDB(db)
		} else {
			fmt.Println("you are not admin, can not use -creatdb")
		}
	}

	if *flagplus == true{
		flagPlus(db, usr.Username)
	}

	checkUsrInfoDB(db, usr.Username)
	check_project_stat(db, usr.Username)
	
	switch len(flag.Args()) {
	case 1:
		switch flag.Args()[0] {
		case "apply", "a":
			insertDB(db, usr.Username)
		case "query", "q":
			QueryDB(db, usr.Username)
		case "editusr", "eu":
			updateUsrInfoDB(db, usr.Username)
		default:
			usage()
		}
	case 2:
		switch flag.Args()[0] {
		case "delete", "d":
			id, _ := strconv.Atoi(flag.Args()[1])
			DeleteDB(db, id, usr.Username)
		case "edit", "e":
			id, _ := strconv.Atoi(flag.Args()[1])
			updateDB(db, id, usr.Username)
		case "outDir", "o":
			exportExcel(db, usr.Username, flag.Args()[1])
		case "mail", "m":
			filepaths, _ := filepath.Abs(flag.Args()[1])
			Sendmail(db, usr.Username, filepaths, bin)
		default:
			usage()
		}
	default:
		usage()
	}
}
