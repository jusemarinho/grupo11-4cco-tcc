package main

import (
	"io/ioutil"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
)

func main() {
	// Defina a URL da função em Python
	err := godotenv.Load()
	if err != nil {
		log.Fatal("Erro ao carregar arquivo .env")
	}

	url := os.Getenv("URL_GOOGLE_FUNCTION")

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		// Crie uma solicitação HTTP
		req, err := http.NewRequest("POST", url, r.Body)
		if err != nil {
			http.Error(w, "Erro ao criar solicitação HTTP", http.StatusInternalServerError)
			return
		}

		// Adicione os cabeçalhos da solicitação original para a nova solicitação
		for k, v := range r.Header {
			req.Header.Add(k, v[0])
		}

		// Envie a solicitação HTTP
		client := &http.Client{}
		resp, err := client.Do(req)
		if err != nil {
			http.Error(w, "Erro ao enviar solicitação HTTP", http.StatusInternalServerError)
			return
		}
		defer resp.Body.Close()

		// Leia a resposta da solicitação HTTP
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			http.Error(w, "Erro ao ler resposta HTTP", http.StatusInternalServerError)
			return
		}

		// Escreva a resposta na resposta HTTP
		w.Header().Set("Content-Type", resp.Header.Get("Content-Type"))
		w.WriteHeader(resp.StatusCode)
		w.Write(body)
	})

	log.Fatal(http.ListenAndServe(":8080", nil))
}
