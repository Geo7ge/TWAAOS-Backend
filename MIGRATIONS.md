# Database Migrations

Acest fișier documentează toate migrările bazei de date și modificările structurale ale proiectului.

## Migration Log

### ✅ 001_initial_schema

**Data:** 2026-04-15  
**Status:** Pending  
**Descriere:** Creează tabelul inițial `users` cu coloanele:

- id (PRIMARY KEY, auto-incrementing)
- email (UNIQUE)
- name
- role
- password
- created_at (timestamp)
- updated_at (timestamp)

**Modificări:**

- Creează tabelul `users`
- Adaugă index pe coloana `email` pentru performanță

**Cum să aplici:**

1. Du-te la Supabase Dashboard
2. Mergi la **SQL Editor**
3. Copiază conținutul din `migrations/001_initial_schema.sql`
4. Execută query-ul

---

## Cum să adaugi o nouă migrație

1. **Creează fișierul:**
   - Crează un nou file: `migrations/XXX_description.sql`
   - Format: `NNN_descriptive_name.sql` (cu numărul secvențial)

2. **Scrie SQL-ul:**

   ```sql
   -- Migration: XXX_description
   -- Description: Ce schimbă această migrație
   -- Date: YYYY-MM-DD
   -- Status: Pending

   -- Your SQL here
   ```

3. **Aplică în Supabase:**
   - SQL Editor → Copiază SQL → Execută

4. **Actualizează acest fișier:**
   - Adaugă secțiunea cu detaliile migrării
   - Marchează status ca ✅ Applied

5. **Commit în git:**
   ```bash
   git add migrations/
   git commit -m "Migration XXX: descriptive message"
   ```

---

## Status

- ✅ Applied - Migrația a fost executată cu succes
- ⏳ Pending - Migrația e gata dar nu a fost executată
- 🔄 In Progress - Se execută migrația
- ❌ Failed - Migrația a eșuat

---

## Cod Migration Best Practices

✅ DO:

- Scrie migrări incrementale (mici, ușor de reversat)
- Adaugă descrieri clare
- Testează în dev înainte de prod
- Versionezi cu numere secvențiale

❌ DON'T:

- Nu modifica migrări deja aplicate
- Nu șterge migrări vechi
- Nu aplica migrări în dezordine
