package main

import (
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"
)

func main() {
	targetHost := os.Getenv("TARGET_HOST_PROXY_ACHEIOBICHO")
	targetPort := os.Getenv("TARGET_PORT_PROXY_ACHEIOBICHO")

	if targetHost == "" || targetPort == "" {
		fmt.Println("As variáveis de ambiente TARGET_HOST e TARGET_PORT devem ser configuradas.")
		return
	}

	proxy := httputil.NewSingleHostReverseProxy(&url.URL{
		Scheme: "http",
		Host:   targetHost + ":" + targetPort,
	})

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("Proxying request: %s %s\n", r.Method, r.URL.Path)
		proxy.ServeHTTP(w, r)
	})

	proxyPort := "3000"
	fmt.Printf("Servidor proxy em execução em :%s\n", proxyPort)
	err := http.ListenAndServe(":"+proxyPort, nil)
	if err != nil {
		fmt.Println("Erro ao iniciar o servidor:", err)
	}
}
