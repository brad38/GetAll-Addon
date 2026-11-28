import pathlib
p=pathlib.Path(r"C:\Users\bradg\Downloads\GetAll-R18\desktop-scope-20261127\Services\GameInstallationSm64PlusOfficial.cs")
s=p.read_text(encoding="utf-8")
old='RunMarioOfficialBash(tools, work, source, "source-integrity", "git diff --exit-code", token);'
new='RunMarioOfficialBash(tools, work, source, "source-integrity",\n                "test \\"$(git rev-parse HEAD)\\" = " + Sm64PlusOfficialCommit + " && git diff --exit-code", token);'
assert old in s;s=s.replace(old,new,1)
p.write_text(s,encoding="utf-8",newline="\n")
