package main

import (
	"fmt"
	"net/http"
	"net/http/httputil"
	"net/url"
	"os"

	"github.com/gorilla/websocket"
)

func main() {
	targetHost := os.Getenv("TARGET_HOST_PROXY_ACHEIOBICHO")
	targetPort := os.Getenv("TARGET_PORT_PROXY_ACHEIOBICHO")

	if targetHost == "" || targetPort == "" {
		fmt.Println("As variáveis de ambiente TARGET_HOST e TARGET_PORT devem ser configuradas.")
		return
	}

	targetURL := &url.URL{
		Scheme: "http",
		Host:   targetHost + ":" + targetPort,
	}

	proxy := httputil.NewSingleHostReverseProxy(targetURL)

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Printf("Proxying request: %s %s\n", r.Method, r.URL.Path)
		proxy.ServeHTTP(w, r)
	})

	upgrader := websocket.Upgrader{
		CheckOrigin: func(r *http.Request) bool {
			return true
		},
	}

	http.HandleFunc("/ws", func(w http.ResponseWriter, r *http.Request) {
		conn, err := upgrader.Upgrade(w, r, nil)
		if err != nil {
			fmt.Println("Erro ao atualizar a conexão WebSocket:", err)
			return
		}
		defer conn.Close()

		targetConn, _, err := websocket.DefaultDialer.Dial(targetURL.String(), nil)
		if err != nil {
			fmt.Println("Erro ao conectar ao destino via WebSocket:", err)
			return
		}
		defer targetConn.Close()

		go func() {
			for {
				messageType, p, err := conn.ReadMessage()
				if err != nil {
					fmt.Println("Erro ao ler mensagem do cliente:", err)
					return
				}
				if err := targetConn.WriteMessage(messageType, p); err != nil {
					fmt.Println("Erro ao escrever mensagem para o destino:", err)
					return
				}
			}
		}()

		for {
			messageType, p, err := targetConn.ReadMessage()
			if err != nil {
				fmt.Println("Erro ao ler mensagem do destino:", err)
				return
			}
			if err := conn.WriteMessage(messageType, p); err != nil {
				fmt.Println("Erro ao escrever mensagem para o cliente:", err)
				return
			}
		}
	})

	proxyPort := "8080"
	fmt.Printf("Servidor proxy em execução em :%s\n", proxyPort)
	err := http.ListenAndServe(":"+proxyPort, nil)
	if err != nil {
		fmt.Println("Erro ao iniciar o servidor:", err)
	}
}
