package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"sync"

	"github.com/PuerkitoBio/goquery"
)


func checkFile(filename string) error {
    _, err := os.Stat(filename)
        if os.IsNotExist(err) {
            _, err := os.Create(filename)
                if err != nil {
                    return err
                }
        }
        return nil
}

func openJson(filename string) ([]NaverQADB, error) {
	data := []NaverQADB{}

	err := checkFile(filename)
	if (err != nil){
		return data, err
	}
	file, err := ioutil.ReadFile(filename)
	if err != nil {
		return data, err
	}

	json.Unmarshal(file, &data)
	return data, nil
}

func writeJson(filename string, data []NaverQADB) error {
	dataBytes, err := json.Marshal(data)
    if err != nil {
		return err
    }

    err = ioutil.WriteFile(filename, dataBytes, 0644)
    if err != nil {
		return err
    }

	return nil
}

type NaverQADB struct {
	ID string `json:"id"`
	Title string `json:"title"`
	Question string `json:"question"`
	Answers []string `json:"answer"`
	Topic string `json:"topic"`
}

func parse(f *os.File) NaverQADB {
	html, err := goquery.NewDocumentFromReader(f)
	if err != nil {
	 	log.Fatal(err)
	}
	
	title := html.Find("div.c-heading__title-inner").Find("div.title").Text()
	title = strings.TrimSpace(title)

	topic := html.Find("a.tag-list__item.tag-list__item--category").Text()
	topic = strings.Join(strings.Split(topic, " ")[2:], " ")

	var temp_question []string
	question := ""
	
	_ = html.Find("div.c-heading__content").Find("div").Each(func(idx int, sel *goquery.Selection){
		t := sel.Text()
		t = strings.TrimSpace(t)

		temp_question = append(temp_question, t)
	})

	question = strings.Join(temp_question, "\n")
	fmt.Println(question)

	var answers []string
	
	_ = html.Find("div._answerListArea").Find("div.answer-content__list._answerList").Each(func(idx int, s *goquery.Selection){
		var temp_answer []string
		answer := ""

		s.Find(".se-module.se-module-text").Find("p").Each(func(idx int, sel *goquery.Selection) {
			t := sel.Text()
			t = strings.TrimSpace(t)

			temp_answer = append(temp_answer, t)
			fmt.Println(t)
		})

		answer = strings.Join(temp_answer, "\n")

		if (answer != ""){
			answers = append(answers, answer)
		}
	})
	
	new := &NaverQADB{
		ID: "",
		Title: title,
		Question: question,
		Answers: answers,
		Topic: topic,
	}

	return *new
}


func main() {
	dataset := flag.String("dataset", "../raw/*", "directory of the raw files.")
	outfile := flag.String("out", "parsed.json", "filename of the output.")

	data, err := openJson(*outfile)
	if err != nil {
		log.Fatal(err)
	}

	files, err := filepath.Glob(*dataset)
	if err != nil {
		log.Fatal(err)
	}
	
	wg := &sync.WaitGroup{}
	for _, file := range files {
		wg.Add(1)
		go func(file string){
			f, err := os.Open(file)
			if err != nil {
				log.Fatal(err)
			}
			defer f.Close()

			newRow := parse(f)
			newRow.ID = strings.Split(strings.Split(file, "/")[len(strings.Split(file, "/"))-1], ".")[0]
			data = append(data, newRow)
			wg.Done()
		}(file)
	}
	wg.Wait()

	writeJson(*outfile, data)
}