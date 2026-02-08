    def _ask_pin(self, title="Token A3 PIN"):
        """Solicita PIN do token de forma segura"""
        dialog = ctk.CTkInputDialog(text="Digite o PIN do Token A3:", title=title)
        pin = dialog.get_input()
        return pin if pin else None
    
    def _encrypt_with_token(self):
        """Criptografa arquivo usando Token A3"""
        if not HAS_TOKEN_A3:
            messagebox.showerror("Token A3", "Módulo Token A3 não instalado!\n\nInstale: pip install PyKCS11 pyscard")
            return
        
        if not self.file_path:
            messagebox.showwarning("Token A3", "Selecione um arquivo primeiro!")
            return
        
        # Detectar token
        self._log(f"🔍 Detectando Token A3...", 'info')
        self.update()
        
        manager = TokenA3Manager()
        success, msg = manager.detect_token()
        
        if not success:
            self._log(f"❌ {msg}", 'error')
            messagebox.showerror("Token A3", f"{msg}\n\nInsira o token A3 e tente novamente.")
            return
        
        self._log(f"✅ {msg}", 'success')
        
        # Solicitar PIN
        pin = self._ask_pin("PIN do Token A3")
        if not pin:
            self._log("⚠️  Operação cancelada", 'info')
            return
        
        # Definir arquivo de saída
        output_path = self.file_path + ".token"
        
        # Desabilitar controles
        self._toggle_controls("disabled")
        self.progress.set(0.3)
        self.update()
        
        try:
            self._log(f"🔒 Criptografando com Token A3...", 'info')
            self.update()
            
            success, msg = manager.encrypt_file_with_token(
                self.file_path,
                output_path,
                pin
            )
            
            self.progress.set(1.0)
            
            if success:
                self._log(f"✅ {msg}", 'success')
                messagebox.showinfo("Sucesso!", f"Arquivo criptografado:\n{output_path}\n\n🔒 Só pode ser aberto com o Token A3 + PIN!")
            else:
                self._log(f"❌ {msg}", 'error')
                messagebox.showerror("Erro", msg)
                
        except Exception as e:
            self._log(f"❌ Erro: {e}", 'error')
            messagebox.showerror("Erro", f"Falha na criptografia:\n{str(e)}")
        finally:
            self._toggle_controls("normal")
            self.progress.set(0)
    
    def _decrypt_with_token(self):
        """Descriptografa arquivo usando Token A3"""
        if not HAS_TOKEN_A3:
            messagebox.showerror("Token A3", "Módulo Token A3 não instalado!\n\nInstale: pip install PyKCS11 pyscard")
            return
        
        if not self.file_path:
            messagebox.showwarning("Token A3", "Selecione um arquivo .token primeiro!")
            return
        
        if not self.file_path.endswith('.token'):
            response = messagebox.askyesno("Confirmar", 
                "O arquivo não tem extensão .token.\nDeseja continuar mesmo assim?")
            if not response:
                return
        
        # Detectar token
        self._log(f"🔍 Detectando Token A3...", 'info')
        self.update()
        
        manager = TokenA3Manager()
        success, msg = manager.detect_token()
        
        if not success:
            self._log(f"❌ {msg}", 'error')
            messagebox.showerror("Token A3", f"{msg}\n\nInsira o token A3 e tente novamente.")
            return
        
        self._log(f"✅ {msg}", 'success')
        
        # Solicitar PIN
        pin = self._ask_pin("PIN do Token A3")
        if not pin:
            self._log("⚠️  Operação cancelada", 'info')
            return
        
        # Definir arquivo de saída
        if self.file_path.endswith('.token'):
            output_path = self.file_path[:-6]  # Remove .token
        else:
            output_path = self.file_path + ".decrypted"
        
        # Desabilitar controles
        self._toggle_controls("disabled")
        self.progress.set(0.3)
        self.update()
        
        try:
            self._log(f"🔓 Descriptografando com Token A3...", 'info')
            self.update()
            
            success, msg = manager.decrypt_file_with_token(
                self.file_path,
                output_path,
                pin
            )
            
            self.progress.set(1.0)
            
            if success:
                self._log(f"✅ {msg}", 'success')
                messagebox.showinfo("Sucesso!", f"Arquivo descriptografado:\n{output_path}")
            else:
                self._log(f"❌ {msg}", 'error')
                if "PIN incorreto" in msg or "token diferente" in msg:
                    messagebox.showerror("Erro de Autenticação", 
                        "Falha ao descriptografar!\n\nPossíveis causas:\n"
                        "• PIN incorreto\n"
                        "• Token diferente do usado para criptografar\n"
                        "• Arquivo corrompido")
                else:
                    messagebox.showerror("Erro", msg)
                    
        except Exception as e:
            self._log(f"❌ Erro: {e}", 'error')
            messagebox.showerror("Erro", f"Falha na descriptografia:\n{str(e)}")
        finally:
            self._toggle_controls("normal")
            self.progress.set(0)

