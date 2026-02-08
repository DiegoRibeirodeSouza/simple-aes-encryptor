comando para reiniciar o serviço do leitor de cartão (PC/SC) é:

bash
sudo systemctl restart pcscd
Depois de reiniciar, você pode verificar se o token foi detectado retirando e plugando ele novamente, e rodando:

bash
opensc-tool -l
(Se tiver instalado, ou apenas observe se a luz do token pisca/acende de forma fixa).

Se precisar ver logs em tempo real para saber o que está acontecendo quando você conecta o token:

bash
sudo journalctl -f -u pcscd
