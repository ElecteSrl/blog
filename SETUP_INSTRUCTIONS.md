# Setup Instructions - Hashnode Sync

## 📋 Come configurare la sincronizzazione automatica

### 1. Aggiungi i file alla repository

Copia questi file nella tua repository `blog`:

```
blog/
├── .github/
│   └── workflows/
│       └── sync-hashnode.yml
├── sync_hashnode.py
└── articles/ (verrà creata automaticamente)
```

### 2. Configura il GitHub Secret

**IMPORTANTE**: Non mettere mai l'API token direttamente nel codice!

1. Vai su GitHub → La tua repository `blog`
2. Clicca su **Settings** → **Secrets and variables** → **Actions**
3. Clicca su **New repository secret**
4. Nome: `HASHNODE_TOKEN`
5. Valore: `8084b026-3613-47c9-aae7-76c15e714392`
6. Clicca su **Add secret**

### 3. Testa la sincronizzazione

#### Test manuale
1. Vai su **Actions** nella tua repository
2. Seleziona il workflow **"Sync Hashnode Articles"**
3. Clicca su **Run workflow** → **Run workflow**
4. Aspetta qualche secondo e verifica che funzioni

#### Automatico ogni ora
Il workflow si eseguirà automaticamente ogni ora e:
- Scaricherà tutti i tuoi articoli da Hashnode
- Li salverà in `articles/YYYY/MM/slug.md`
- Farà commit automatico solo se ci sono modifiche

### 4. Struttura degli articoli

Gli articoli verranno salvati così:

```
articles/
├── 2025/
│   ├── 01/
│   │   ├── primo-articolo.md
│   │   └── secondo-articolo.md
│   └── 10/
│       └── articolo-ottobre.md
```

Ogni file avrà:
- **Frontmatter YAML** con metadati (titolo, tags, date, canonical URL)
- **Contenuto markdown** completo dell'articolo

### 5. Verifica

Dopo il primo run, dovresti vedere:
- ✅ Cartella `articles/` creata
- ✅ File markdown degli articoli
- ✅ Commit automatico da GitHub Actions

## 🔧 Troubleshooting

**Il workflow non parte?**
- Verifica che il secret `HASHNODE_TOKEN` sia configurato correttamente
- Controlla i logs in **Actions**

**Errore API?**
- Verifica che l'API token sia valido su https://hashnode.com/settings/developer

**Nessun commit?**
- Normale se non ci sono nuovi articoli o modifiche

## 📝 Note

- Il workflow usa l'API ufficiale di Hashnode v2
- Scarica fino a 50 articoli (modificabile nello script)
- Preserva il link canonical al tuo blog principale
- Non modifica nulla su Hashnode, solo legge

---

Fatto! 🚀
