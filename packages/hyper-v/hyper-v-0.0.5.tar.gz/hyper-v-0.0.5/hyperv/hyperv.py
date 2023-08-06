from base64 import decode
from distutils.log import debug
from tempfile import template
import winrm
import re


class HyperV:
    def __init__(
        self,
        env_prefix = "",
        storage_root = '''C:\\template.vmcx''',
        vm_template_pach = '',
        host = '',
        user = '',
        password = '',
        debug = False
    ) -> None:

        self.env_prefix = env_prefix
        self.storage_root = storage_root
        self.vm_template_pach = vm_template_pach

        self.host = host
        self.user = user
        self.password = password

        self.debug = debug

        # Создаём сессию для работы с гипервизором
        self.session = winrm.Session(self.host, auth=(self.user, self.password))


    # Поиск шаблона vmcx в папке с шаблоном виртуальной машины

    @property
    def get_vmcx(self):

        ps = f"Get-ChildItem -Path '{self.vm_template_pach}' -Include *.vmcx -File -Recurse -ErrorAction SilentlyContinue"
        vmcx = self.session.run_ps(ps)
        return re.findall(r'[\w-]*.vmcx', vmcx.std_out.decode('utf-8'))[0]


    # Поиск имени шаблона виртуалки
    def get_template_name(self, vmcx):
        ps = f"""
        $TempVM = (Compare-VM -Path '{self.vm_template_pach}\Virtual Machines\{vmcx}').VM
        $TempVM | Select VMName | Select -ExpandProperty "VMName"
        """
        # print("Template Name",ps)
        r = self.session.run_ps(ps)
        # print(r.std_out.decode('utf-8').split("\r\n"))
        result = r.std_out.decode('utf-8').split("\r\n")[0]

        # print('template_name ==>', result)
        return result
    

    # Создание виртуалок
    def create_vm(self, name='', ip='', cpu=1, ram=1, template_name='', vmcx =''):
        if vmcx == '':
            vmcx = self.get_vmcx
        if template_name == '':
            template_name = self.get_template_name(vmcx)
        
        import_from=f"{self.vm_template_pach}\Virtual Machines\{vmcx}"
        vm_patch=f"{self.storage_root}\{self.env_prefix}\{self.env_prefix}-{name}"
        vm_name=f"{self.env_prefix}-{name}_({ip})"

        # Генерируем powershell скрипт
        ps_script =  f'''
        Write-Host "Creating VM {vm_name}"
        Import-VM -Path "{import_from}" -Copy -GenerateNewId -SnapshotFilePath "{vm_patch}" -VhdDestinationPath "{vm_patch}" -SmartPagingFilePath "{vm_patch}"
        Set-VM -Name "{template_name}" -ProcessorCount {cpu} -StaticMemory -MemoryStartupBytes {ram}Gb
        Rename-VM "{template_name}" -NewName "{vm_name}"
        Write-Host 'Done'
        '''
        # print("Create VM",ps_script)
        r = self.session.run_ps(ps_script)
        # print('create VM status_code:',r.status_code)
        # print('create VM:',r.std_out.decode('utf-8'))
        if 'Done' in r.std_out.decode('utf-8'):
            return True
        return False


    # Включение виртуалок
    def start_vm(self,name='', ip=''):
        vm_name=f"{self.env_prefix}-{name}_({ip})"
        # Генерируем powershell скрипт
        ps_script =  f'''
        Start-VM -Name "{vm_name}"
        '''
        # print("Start VM",ps_script)
        r = self.session.run_ps(ps_script)
        # print('start VM status_code:', r.status_code)
        # print('start VM:',r.std_out.decode('utf-8'))
        if r.status_code == '1':
            return False
        return True

    # Запрос свободной памяти на гипервизоре
    @property
    def get_free_memory(self):
        # print('get_free_memory')
        ps = "(Get-WMIObject Win32_OperatingSystem).FreePhysicalMemory / 1MB"
        r = self.session.run_ps(ps)
        
        if r.status_code == 0:
            free_memory = round(float(r.std_out.decode('utf-8').replace(',','.')), 2)
        else:
            return False
        return free_memory


    # Создать снапшот кластера по его маске
    def start_snapshot(self, snapshot_name='Clear_OS'):
        ps_script = f'''
        Get-VM -Name {self.env_prefix}* | Sort Name | Foreach-Object ''' + '''{ $_ | Checkpoint-VM -SnapshotName''' + f''' "{snapshot_name}" -AsJob''' + ' }'
        # print(ps_script)
        r = self.session.run_ps(ps_script)
        # print('start:',r.status_code)
        # print('start:',r.std_out.decode('utf-8'))

