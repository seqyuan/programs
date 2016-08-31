package main

//by ahworld seqyuan
import (
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

func usage() {
	fmt.Printf("\n\nProgram: applyProject (Tools for apply project)\nVersion: 0.0.1-20160829\n\nUsage:\tapplyProject <command> [options]\n\n")
	fmt.Printf("Command:\n")
	fmt.Printf("    a|pply                  apply a project\n")
	fmt.Printf("    q|query                 query the apply projects of your groups\n")
	fmt.Printf("    e|edit [id]             reEdit the apply project\n")
	fmt.Printf("    d|delete [id]           delete the apply project\n")
	fmt.Printf("    o|outDir [dir]          dir to export apply projects excel file(then you can send it by email)\n")
	fmt.Printf("    m|mail [out.xlsx]       send the Excel to leader@yodagene.com\n\n")
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

func exportExcel(db *sql.DB, usr string, outDir string) {
	var (
		xlsxFile *xlsx.File
		sheet    *xlsx.Sheet
		//	row *xlsx.Row
		//	cell *xlsx.Cell
		err error
	)
	var (
		id           int
		user         string
		name         string
		groups       string
		project_type string
		project_name string
		start_time   string
		end_time     string
		project_txt  string
		need_time    string
	)

	row := db.QueryRow("select groups from usrInfo where user = ?", usr)
	err = row.Scan(&groups)

	xlsxFile = xlsx.NewFile()
	sheet1 := fmt.Sprintf("%s下单申请", groups)
	sheet, _ = xlsxFile.AddSheet(sheet1)

	rows, err := db.Query("select * from applyProject where groups = ? order by user", groups)
	defer rows.Close()
	if err != nil {
		fmt.Println("你们组没有要申请的项目！")
		defer rows.Close()
		os.Exit(1)
	}
	slice := []string{"任务类型", "任务单名称", "信息负责人", "信息起始日期", "信息截止日期", "分析内容", "估时"}
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

	ids := make([]int, 100)
	i := 0
	for rows.Next() {
		err = rows.Scan(&id, &user, &name, &groups, &project_type, &project_name, &start_time, &end_time, &project_txt, &need_time)
		ids[i] = id
		i = i + 1

		checkErr(err)
		xlsrow = sheet.AddRow()
		slice := []string{project_type, project_name, name, start_time, end_time, project_txt, need_time}
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

	t := time.Now()
	/*fmt.Printf("%d-%02d-%02dT%02d:%02d:%02d-00:00\n",
	  t.Year(), t.Month(), t.Day(),
	  t.Hour(), t.Minute(), t.Second())
	*/
	outExcel := fmt.Sprintf("%s/%s_%d-%02d-%02dT%02d-%02d.xlsx", outDir, sheet1, t.Year(), t.Month(), t.Day(), t.Hour(), t.Minute())
	err = xlsxFile.Save(outExcel)
	if err != nil {
		fmt.Printf("save xlsx file fail , error : %s", err.Error())
		fmt.Printf("提供一个可写的目录以供输出excel")
		//return
	}
	//	defer rows.Close()
	defer db.Close()

	for _, value := range ids[:i] {
		stmt, err := db.Prepare("delete from applyProject where id=?")
		checkErr(err)
		_, err = stmt.Exec(value)
		checkErr(err)
	}

	defer db.Close()
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
		cmdString := fmt.Sprintf("ssh c0008 2> /dev/null \"/yodagene/share/software/install/Python-3.3.2/bin/python3 %s/sendEmail.py %s %s\"", bin, pass, xlsxfile)
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
	//fmt.Println("\nid\t集群账号\t信息负责人\t组别\t项目类别\t任务单名称\t起始时间\t结束时间\t分析内容\t估时")
	fmt.Println("\nid\t组别\t项目类别\t信息负责人\t任务单名称\t起始时间\t结束时间\t分析内容\t估时")
	var (
		id           int
		user         string
		name         string
		groups       string
		project_type string
		project_name string
		start_time   string
		end_time     string
		project_txt  string
		need_time    string
	)
	for rows.Next() {
		err := rows.Scan(&id, &user, &name, &groups, &project_type, &project_name, &start_time, &end_time, &project_txt, &need_time)
		checkErr(err)
		//fmt.Printf("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", id, user, name, groups, project_type, project_name, start_time, end_time, project_txt, need_time)
		fmt.Printf("%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", id, groups, project_type, name, project_name, start_time, end_time, project_txt, need_time)
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
	//drp_tb_sql := "drop table if exists applyProject"
	//_, err := db.Exec(drp_tb_sql)
	sqlStmt := `
	create table if not exists applyProject (
		id integer unique not null primary key,
		user string,
		name string,
		groups string,
		project_type string,
		project_name string unique not null,
		start_time string,
		end_time string,
		project_txt string,
		need_time string
		);
		`
	_, err := db.Exec(sqlStmt)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
	//usr, _ := user.Current()
	//QueryDB(db, usr.Username)
}
func QueryDB(db *sql.DB, usr string) {
	//查询所在组申请项目
	var groups string
	row := db.QueryRow("select groups from usrInfo where user = ?", usr)
	err := row.Scan(&groups)

	rows, err := db.Query("select * from applyProject where groups = ? order by user", groups)
	defer rows.Close()
	if err == nil {
		Printrows(rows)
		defer rows.Close()
	}
	defer rows.Close()
}

func CreatUsrInfoDB(db *sql.DB) {
	//drp_tb_sql := "drop table if exists usrInfo"
	//_, err := db.Exec(drp_tb_sql)
	sqlStmt := `
	create table if not exists usrInfo (
		id integer unique not null primary key,
		user string unique not null,
		name string,
		groups string,
		email string
		);
		`
	_, err := db.Exec(sqlStmt)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}
	//QueryUsrInfoDB(db)
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
	if name == "" || groups == "" || email == "" {
		fmt.Println("你需要补全 姓名组别邮箱信息 才能使用这个程序！")
		updateUsrInfoDB(db, usr)
	}
	//fmt.Println(name, groups, email)
}
func insertUsrInfoDB(db *sql.DB, usr string) {
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
		"0": "分析二组",
		"1": "医口分析组",
		"2": "转录调控组",
		"3": "分析一组",
		"4": "denovo组",
		"5": "DNA组",
		"6": "质控组",
	}
	for groups == "" {
		i := myinput("请输入你的组别:\n分析二组 [0]\n医口分析组 [1]\n转录调控组 [2]\n分析一组 [3]\ndenovo组 [4]\nDNA组 [5]\n质控组 [6]\n\n如果你的组不在列表里请直接输入组名")
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
		match, _ := regexp.MatchString("@yodagene.com", email)
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
	defer db.Close()
	os.Exit(1)
}

func updateUsrInfoDB(db *sql.DB, usr string) {
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
	if name == "" {
		name = myinput("请输入你的姓名:")
	}
	if groups == "" {
		groupss := map[string]string{
			"0": "分析二组",
			"1": "医口分析组",
			"2": "转录调控组",
			"3": "分析一组",
			"4": "denovo组",
			"5": "DNA组",
			"6": "质控组",
		}
		for groups == "" {
			i := myinput("请输入你的组别:\n分析二组 [0]\n医口分析组 [1]\n转录调控组 [2]\n分析一组 [3]\ndenovo组 [4]\nDNA组 [5]\n质控组 [6]\n\n如果你的组不在列表里请直接输入组名")
			groupsss, err := groupss[i]
			if err != true {
				groups = i
				fmt.Println("你输入了一个新的组名")
			} else {
				groups = groupsss
			}
		}
	}
	if email == "" {
		for email == "" {
			email = myinput("请输入你的邮箱:")
			match, _ := regexp.MatchString("@yodagene.com", email)
			if match == false {
				email = ""
			}
		}
	}

	stmt, err := db.Prepare("update usrInfo set name=?, groups=?, email=? where user=?")
	checkErr(err)
	_, err = stmt.Exec(name, groups, email, usr)
	checkErr(err)
	defer db.Close()
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
}

func insertDB(db *sql.DB, usr string) {
	//插入数据
	var (
		name         string
		groups       string
		project_type string
		project_name string
		start_time   string
		end_time     string
		project_txt  string
		need_time    string
	)
	row := db.QueryRow("select name, groups from usrInfo where user = ?", usr)
	err := row.Scan(&name, &groups)

	protypes := map[string]string{
		"0": "hic",
		"1": "epi",
		"2": "rna",
		"3": "dna",
		"4": "qc",
	}
	for project_type == "" {
		i := myinput("请输入你申请的项目类型:\nhic [0]\nepi [1]\nrna [2]\ndna [3]\nqc [4]\n\n如果项目类型不在列表里请直接输入项目类型")
		project_types, err := protypes[i]
		if err != true {
			project_type = i
			fmt.Println("你输入了一个新的项目类型")
		} else {
			project_type = project_types
		}
	}
	project_name = myinput("任务单名称:")
	start_time = myinput("信息起始日期(格式: 2016/08/29):")
	end_time = myinput("信息截止日期(格式: 2016/08/29):")
	project_txt = myinput("分析内容:")
	if need_time == "" {
		for need_time == "" {
			need_time = myinput("估时(格式:2h):")
			match, _ := regexp.MatchString("h$", need_time)
			if match == false {
				need_time = ""
			}
		}
	}
	need_time = fmt.Sprintf("%s", strings.Trim(need_time, "h"))
	stmt, err := db.Prepare("insert into applyProject(user,name,groups,project_type, project_name, start_time, end_time, project_txt, need_time) values(?,?,?,?,?,?,?,?,?)")
	checkErr(err)
	res, err := stmt.Exec(usr, name, groups, project_type, project_name, start_time, end_time, project_txt, need_time)
	checkErr(err)
	_, err = res.LastInsertId()
	checkErr(err)
	defer db.Close()
}

func updateDB(db *sql.DB, id int, linuxUser string) {
	//更新数据
	//fmt.Println("id", "集群账号", "姓名", "组别", "项目类别", "任务单名称", "起始时间", "结束时间", "分析内容", "估时")
	var (
		user             string
		name             string
		groups           string
		project_type     string
		project_type_new string
		project_name     string
		project_name_new string
		start_time       string
		start_time_new   string
		end_time         string
		end_time_new     string
		project_txt      string
		project_txt_new  string
		need_time        string
		need_time_new    string
	)

	stmt, err := db.Prepare("select user from applyProject where id=?")
	err = stmt.QueryRow(id).Scan(&user)
	fmt.Println("qwer")
	if err != nil {
		fmt.Println("这个任务单不存在, 如果要修改请输入一个正确的任务单！")
		defer db.Close()
		os.Exit(1)
	}

	if linuxUser != user {
		fmt.Println("你不是这个任务单的申请人,不能对这个任务单进行操作！")
		defer db.Close()
		os.Exit(1)
	}

	stmt, err = db.Prepare("select * from applyProject where id=?")
	err = stmt.QueryRow(id).Scan(&id, &user, &name, &groups, &project_type, &project_name, &start_time, &end_time, &project_txt, &need_time)

	//rows := db.QueryRow("select * from usrInfo where id = ?", id)
	//err = rows.Scan(&id, &user, &name, &groups, &project_type, &project_name, &start_time, &end_time, &project_txt, &need_time)
	checkErr(err)

	protypes := map[string]string{
		"0": "hic",
		"1": "epi",
		"2": "rna",
		"3": "dna",
		"4": "qc",
	}
	i := myinput("请输入你申请的项目类型:\nhic [0]\nepi [1]\nrna [2]\ndna [3]\nqc [4]\n\n如果你的项目类型不在列表里请直接输入项目类型")
	protypess, ok := protypes[i]
	if ok != true {
		project_type_new = i
		fmt.Println("你输入了一个新的项目类型")
	} else {
		project_type_new = protypess
	}

	project_names := myinput(fmt.Sprintf("任务单名称: %s [0]", project_name))
	if project_names == "0" {
		project_name_new = project_name
	} else {
		project_name_new = project_names
	}

	start_times := myinput(fmt.Sprintf("信息起始日期(格式: 2016/08/29): %s [0]", start_time))
	if start_times == "0" {
		start_time_new = start_time
	} else {
		start_time_new = start_times
	}

	end_times := myinput(fmt.Sprintf("信息截止日期(格式: 2016/08/29): %s [0]", end_time))
	if end_times == "0" {
		end_time_new = end_time
	} else {
		end_time_new = end_times
	}

	project_txts := myinput(fmt.Sprintf("分析内容: %s [0]", project_txt))
	if project_txts == "0" {
		project_txt_new = project_txt
	} else {
		project_txt_new = project_txts
	}

	need_times := myinput(fmt.Sprintf("估时: %s [0]", need_time))
	if need_times == "0" {
		need_time_new = need_time
	} else {
		need_time_new = need_times
	}

	stmt, err = db.Prepare("update applyProject set project_type=?, project_name=?, start_time=?, end_time=?, project_txt=?, need_time=? where id =?")
	checkErr(err)
	_, err = stmt.Exec(project_type_new, project_name_new, start_time_new, end_time_new, project_txt_new, need_time_new, id)
	checkErr(err)
	defer db.Close()
	os.Exit(1)
}

func main() {
	file, _ := exec.LookPath(os.Args[0])
	filepaths, _ := filepath.Abs(file)
	bin := filepath.Dir(filepaths)

	DBfile := bin + "/tmp/applyProject.db"
	db, err := sql.Open("sqlite3", DBfile)
	checkErr(err)
	defer db.Close()
	usr, _ := user.Current()

	//CreatUsrInfoDB(db)
	//CreatDB(db)

	checkUsrInfoDB(db, usr.Username)
	defer db.Close()

	switch len(os.Args) {
	case 2:
		switch os.Args[1] {
		case "apply", "a":
			insertDB(db, usr.Username)
		case "query", "q":
			QueryDB(db, usr.Username)
		default:
			usage()
		}
	case 3:
		switch os.Args[1] {
		case "delete", "d":
			id, _ := strconv.Atoi(os.Args[2])
			DeleteDB(db, id, usr.Username)
		case "edit", "e":
			id, _ := strconv.Atoi(os.Args[2])
			updateDB(db, id, usr.Username)
		case "outDir", "o":
			exportExcel(db, usr.Username, os.Args[2])
		case "mail", "m":
			filepaths, _ := filepath.Abs(os.Args[2])
			Sendmail(db, usr.Username, filepaths, bin)
		default:
			usage()
		}
	default:
		usage()
	}
}
