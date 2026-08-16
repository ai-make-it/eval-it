#!/usr/bin/env bash
#
# Carica sito/ nella sottocartella del dominio, via SSH.
#
#   ./deploy.sh              prova a vuoto: dice cosa cambierebbe, non tocca nulla
#   ./deploy.sh --conferma   carica davvero
#
# La configurazione sta nelle variabili qui sotto, sovrascrivibili
# dall'ambiente o da un file deploy.conf accanto a questo script
# (deploy.conf non entra in git: contiene il percorso della chiave).
#
#   SG_UTENTE=uXXXXXX-YYYYY ./deploy.sh --conferma
#
# Perche' la prova a vuoto e' il comportamento predefinito: rsync qui gira
# con --delete, e un percorso remoto sbagliato su un hosting condiviso
# cancella un sito. Si guarda cosa farebbe, poi si conferma.

set -euo pipefail
cd "$(dirname "$0")"

[ -f deploy.conf ] && . ./deploy.conf

SG_HOST="${SG_HOST:-ssh.ai-make.it}"
SG_PORTA="${SG_PORTA:-18765}"
SG_UTENTE="${SG_UTENTE:-}"
SG_CHIAVE="${SG_CHIAVE:-$HOME/.ssh/siteground-ai-make-it}"
SG_REMOTO="${SG_REMOTO:-www/ai-make.it/public_html/dizionario}"

rosso() { printf '\033[31m%s\033[0m\n' "$*" >&2; }

if [ -z "$SG_UTENTE" ]; then
  rosso "Manca SG_UTENTE (l'utente SSH di SiteGround, tipo u1234-56789)."
  rosso "Mettilo in deploy.conf oppure passalo nell'ambiente."
  exit 1
fi

if [ ! -f "$SG_CHIAVE" ]; then
  rosso "Chiave SSH non trovata: $SG_CHIAVE"
  rosso "Impostala con SG_CHIAVE, oppure creane una da Site Tools > Devs > SSH."
  exit 1
fi

if [ ! -f sito/index.html ]; then
  rosso "sito/ non c'e' o e' incompleto. Lancia prima:"
  rosso "  python src/validate.py && python src/build.py && python src/sito.py"
  exit 1
fi

# Il guardrail che conta: --delete su public_html cancellerebbe il sito.
# Si carica solo dentro una sottocartella dedicata.
case "$SG_REMOTO" in
  */public_html|*/public_html/|public_html|public_html/)
    rosso "SG_REMOTO punta alla radice del sito: $SG_REMOTO"
    rosso "Questo script gira con --delete e va usato solo su una"
    rosso "sottocartella dedicata, tipo www/ai-make.it/public_html/dizionario."
    exit 1 ;;
esac

SSH="ssh -p $SG_PORTA -i $SG_CHIAVE -o StrictHostKeyChecking=accept-new"
DESTINAZIONE="$SG_UTENTE@$SG_HOST:$SG_REMOTO/"

if [ "${1:-}" = "--conferma" ]; then
  ASCIUTTO=""
  echo "Carico su $DESTINAZIONE"
else
  ASCIUTTO="--dry-run"
  echo "Prova a vuoto verso $DESTINAZIONE (niente viene scritto)."
  echo "Per caricare davvero: ./deploy.sh --conferma"
fi
echo

$SSH "$SG_UTENTE@$SG_HOST" "mkdir -p '$SG_REMOTO'"

rsync -rlvz --checksum --delete $ASCIUTTO \
  --chmod=D755,F644 \
  --exclude ".DS_Store" \
  -e "$SSH" \
  sito/ "$DESTINAZIONE"

if [ -z "$ASCIUTTO" ]; then
  # --chmod copre i file caricati; questo raddrizza quelli gia' presenti.
  $SSH "$SG_UTENTE@$SG_HOST" \
    "find '$SG_REMOTO' -type d -exec chmod 755 {} + ; \
     find '$SG_REMOTO' -type f -exec chmod 644 {} +"
  echo
  echo "Fatto. Restano due cose da fare a mano, una volta sola:"
  echo "  1. dichiarare la sitemap nel robots.txt della radice del dominio:"
  echo "     Sitemap: https://ai-make.it/dizionario/sitemap.xml"
  echo "  2. inviare la sitemap in Google Search Console."
fi
