def change_mac_address(self):
        try:
            
            adapter_name = self.get_wireless_interface()
            if not adapter_name:
                raise Exception("No wireless adapter found")

            
            new_mac = [random.randint(0x00, 0xff) for _ in range(6)]
            new_mac[0] &= 0xfe  
            new_mac[0] |= 0x02  
            mac_address = ''.join([f"{x:02x}" for x in new_mac]) 

            disable_cmd = f'netsh interface set interface "{adapter_name}" admin=disable'
            subprocess.run(disable_cmd, shell=True, check=True, encoding='cp1252')
            time.sleep(2)

            reg_path = (
                'HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\Class\\'
                '{4D36E972-E325-11CE-BFC1-08002BE10318}\\0000'
            )
            reg_cmd = f'reg add "{reg_path}" /v NetworkAddress /t REG_SZ /d {mac_address} /f'
            subprocess.run(reg_cmd, shell=True, check=True, encoding='cp1252')
            time.sleep(1)

            enable_cmd = f'netsh interface set interface "{adapter_name}" admin=enable'
            subprocess.run(enable_cmd, shell=True, check=True, encoding='cp1252')
            time.sleep(3)

            return True

        except subprocess.CalledProcessError as e:
            self.update_progress(f"Error executing command: {str(e)}")
            return False
        except Exception as e:
            self.update_progress(f"Error changing MAC address: {str(e)}")
            return False
