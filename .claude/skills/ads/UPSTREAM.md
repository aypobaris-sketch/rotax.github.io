# Kaynak

Bu klasör ve `ads-*` kardeş skill'leri **Claude Ads** projesinden gelir.

- Depo: https://github.com/AgriciDaniel/claude-ads
- Sürüm: 2.0.1
- Commit: 669c7608ecb50dd95c941a71fa3ca0a1c0e40512
- Lisans: MIT (bkz. `LICENSE`)
- Kurulum: `bash install.sh --source=local --no-deps --skill-dir=.claude/skills --agent-dir=.claude/agents`

Dosyalar elle düzenlenmedi. Güncellemek için depoyu tekrar çekip aynı
komutu çalıştır; `.claude/skills/.claude-ads-claude.manifest` hangi
dosyaların bu pakete ait olduğunu tutar.

Python yardımcıları (`scripts/`) kuruldu ama bağımlılıkları kurulmadı
(`--no-deps`). Gerekirse `.claude/skills/ads/requirements.lock` ile
kurulur; `.venv` klasörü `.gitignore`'da.
