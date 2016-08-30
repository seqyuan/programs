package main

import (
	"bufio"
	"fmt"
	"github.com/tealeg/xlsx"
	"os"
	"strings"
)

func main() {

	if len(os.Args) != 3 {
		fmt.Printf("Usage : %s inFile outFile\n", os.Args[0])
		return
	}

	inFileName := os.Args[1]
	outFileName := os.Args[2]
	inFh, err := os.OpenFile(inFileName, os.O_RDONLY, 0755)
	if err != nil {
		fmt.Printf("open file %s fail , error : %s", inFileName, err.Error())
		return
	}

	xlsxFile := xlsx.NewFile()
	sheet, _ := xlsxFile.AddSheet("sheet1")

	scanner := bufio.NewScanner(inFh)
	for scanner.Scan() {
		arr := strings.Split(scanner.Text(), "\t")
		row := sheet.AddRow()
		for _, s := range arr {
			cell := row.AddCell()
			cell.Value = s
		}
	}

	err = xlsxFile.Save(outFileName)
	if err != nil {
		fmt.Printf("save xlsx file fail , error : %s", err.Error())
		return
	}

}
