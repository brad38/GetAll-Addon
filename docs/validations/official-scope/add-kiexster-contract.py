import pathlib,json
root=pathlib.Path(__file__).resolve().parent
p=root/'restore-msys-msvc-gt5-recipes.py'
s=p.read_text(encoding='utf-8')
s='\n'.join(line for line in s.splitlines() if not (line.startswith('specs.append(json.loads(') and 'god-of-war-kiexster-d1d11ec-official-installer' in line))+'\n'
payload=json.loads('''{"project_id":"god-of-war-recomp","tag":"build-d1d11ec","build_profile":"god-of-war-kiexster-d1d11ec-official-installer","required_files":["source.zip","README.md"],"manual_steps":"Selecione sua ISO original americana de God of War para PS2 (SCUS_973.99). O All-Fix executa os scripts oficiais de extração, compilação e execução da KIexster, sem alterar os fontes do projeto. Se faltarem ferramentas Microsoft, o download exige aceite explícito dos termos. A primeira compilação pode demorar; nenhum jogo está incluído.","preparation_media":[{"id":"original-disc","kind":"file","extensions":[".iso"],"version":"ISO original americana de God of War PS2 (SCUS_973.99)."}],"upstream_commit":"d1d11ec545c3baf2f3fc17e2df4247ac4b732d5c"}''')
addition='specs.append(json.loads('+repr(json.dumps(payload,ensure_ascii=False))+'))\n'
marker='replacements=policy["approved_recipe_replacements"]'
s=s.replace(marker,addition+marker,1)
p.write_text(s,encoding='utf-8',newline='\n')
exec(compile(s,str(p),'exec'),{'__file__':str(p),'__name__':'__main__'})
