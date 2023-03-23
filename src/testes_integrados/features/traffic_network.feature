Feature: Feature Description: Segurança do tráfego de rede

Cenário: Verificar se o tráfego de rede está criptografado
    Given que o tráfego de rede está sendo enviado e recebido pela VPC
    When eu verifico o status da criptografia do tráfego
    Then todo o tráfego de rede deve estar criptografado
