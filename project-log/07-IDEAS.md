# 07 — IDEAS (Icebox / boîte à idées)

> Pour capturer une idée en 5 secondes pendant que tu travailles, SANS dérailler
> le sprint en cours. Ici on **capture**, on ne **décide pas**.
>
> Règle d'or : rien dans ce fichier n'est sur le chemin critique tant que ce n'est
> pas **promu** vers `02-TODO.md`. Noter une idée ≠ s'engager dessus.
> Source initiale : `docs/ROADMAP.md` (« Beyond v1.0 ») + `docs/PROJECT_DOSSIER.md`.

## Triage (tous les 14 jours, à la fin du sprint)
- **Promote** → ça passe dans le backlog de `02-TODO.md` (= candidat sérieux)
- **Keep** → bonne idée mais pas maintenant, reste ici
- **Drop** → on tue, on barre (on garde la trace, on ne supprime pas)

## Boîte à idées
| Date | Idée | Pourquoi ça pourrait compter | Projet | Statut |
|------|------|------------------------------|--------|--------|
| 2026-05-23 | Voice CV intake (Telegram voice → Whisper → extraction) | Beaucoup de travailleurs informels écrivent peu — la voix baisse la barrière | Trov | keep |
| 2026-05-23 | Job posting flow (stored job posts → reverse candidate search) | Aujourd'hui on matche candidats↔requêtes ; les posts stockés ouvrent la recherche inverse | Trov | keep |
| 2026-05-23 | Taxonomie de compétences propre au marché khmer | Améliore le matching au-delà de l'embedding générique | Trov | keep |
| 2026-05-23 | Partenariats universités / NGO (placement de diplômés) | Source de volume + crédibilité institutionnelle | Trov | keep |
| 2026-05-23 | Template de réplication Laos / Myanmar / Vietnam | Même problème, mêmes marchés SEA sans acteur spécialisé | Trov | keep |
| 2026-05-23 | Déploiement Ollama local (100% offline) | Souveraineté données + coût zéro API en mode dégradé | Trov | keep |

<!-- Statuts : new · keep · promoted · ~~dropped~~ -->

## 🚩 At-risk — revue OBLIGATOIRE avant toute implémentation
> Une idée ici touche un domaine sensible (santé · finance · juridique · données
> personnelles). Elle ne passe JAMAIS directement en `02-TODO`, même « promoted ».

| Idée | Pourquoi c'est sensible (failure mode) | Forme dégradée seule acceptable | Revue requise | Statut |
|------|----------------------------------------|----------------------------------|---------------|--------|
| Cross-channel relayed messaging (employer ↔ candidate) | Relayer des messages = données perso + risque d'usage hors-plateforme ; sans audit log = non-conformité LPDP | Relais via la plateforme uniquement, audit log LPDP en place AVANT activation, pas de partage de numéro | légale (LPDP) | keep |
| Rating system v2 (verification badges) | Un badge mal attribué fausse la confiance = cœur du moat | Critères de badge validés + immuabilité conservée + gouvernance 2/3 | produit + légale | keep |

<!-- Règle : tant que la "revue requise" n'est pas faite ET validée par Alex, l'idée
reste ici — jamais dans le sprint. -->
