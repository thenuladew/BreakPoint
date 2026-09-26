#!/usr/bin/env bash
# ============================================================
# BREAKPOINT CTF – Management Script
# ============================================================
# Usage:
#   ./manage.sh <command>
#
# Commands:
#   build       Build all Docker images
#   up          Start all services (detached)
#   down        Stop and remove containers (keeps volumes)
#   reset       Full teardown including volumes (wipes all data)
#   logs        Tail logs for all services (Ctrl+C to stop)
#   status      Show running container status
#   test        Run the full automated test suite
#   shell <svc> Open a shell inside a running container
#   gen-env     Copy .env.example → .env if .env doesn't exist
#   help        Show this help message
# ============================================================

set -euo pipefail

COMPOSE="docker compose"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Colour helpers ────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
CYAN='\033[0;36m'; BOLD='\033[1m'; RESET='\033[0m'

info()    { echo -e "${CYAN}[INFO]${RESET}  $*"; }
success() { echo -e "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo -e "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo -e "${RED}[ERROR]${RESET} $*" >&2; exit 1; }

# ── Prereq checks ────────────────────────────────────────────
check_deps() {
  command -v docker &>/dev/null || error "docker not found. Install Docker Engine first."
  docker compose version &>/dev/null || error "docker compose plugin not found."
}

# ── .env guard ───────────────────────────────────────────────
check_env() {
  if [[ ! -f "$PROJECT_ROOT/.env" ]]; then
    warn ".env not found. Run './manage.sh gen-env' first, then edit .env with your values."
    exit 1
  fi
}

# ── Commands ─────────────────────────────────────────────────
cmd_gen_env() {
  if [[ -f "$PROJECT_ROOT/.env" ]]; then
    warn ".env already exists. Delete it manually if you want to regenerate."
  else
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    success ".env created from .env.example. Please edit it before running 'up'."
  fi
}

cmd_build() {
  check_env
  info "Building all Docker images…"
  $COMPOSE --project-directory "$PROJECT_ROOT" build --no-cache
  success "Build complete."
}

cmd_up() {
  check_env
  info "Starting all services in detached mode…"
  $COMPOSE --project-directory "$PROJECT_ROOT" up -d
  echo ""
  success "BreakPoint CTF is running!"
  echo -e "${BOLD}  CTF Platform  →  http://localhost:8080${RESET}"
  echo -e "${BOLD}  Stage 1        →  http://localhost:8081${RESET}"
  echo -e "${BOLD}  Stage 2        →  http://localhost:8082${RESET}"
  echo -e "${BOLD}  File Share     →  http://localhost:8084${RESET}"
  echo -e "${BOLD}  Stage 6 (gated)→  http://localhost:8090${RESET}"
}

cmd_down() {
  info "Stopping containers (volumes preserved)…"
  $COMPOSE --project-directory "$PROJECT_ROOT" down
  success "Containers stopped."
}

cmd_reset() {
  warn "This will DESTROY all containers AND volumes (all CTF data will be lost)."
  read -r -p "Type 'yes' to confirm: " confirm
  [[ "$confirm" == "yes" ]] || { info "Aborted."; exit 0; }
  $COMPOSE --project-directory "$PROJECT_ROOT" down -v --remove-orphans
  success "Full reset complete."
}

cmd_logs() {
  $COMPOSE --project-directory "$PROJECT_ROOT" logs -f --tail=50
}

cmd_status() {
  $COMPOSE --project-directory "$PROJECT_ROOT" ps
}

cmd_test() {
  check_env
  info "Running automated test suite…"
  pushd "$PROJECT_ROOT/tests" > /dev/null
  bash run_all_tests.sh
  popd > /dev/null
}

cmd_shell() {
  local svc="${1:-}"
  [[ -z "$svc" ]] && error "Usage: ./manage.sh shell <service-name>"
  $COMPOSE --project-directory "$PROJECT_ROOT" exec "$svc" /bin/sh
}

cmd_help() {
  sed -n '/^# Usage/,/^# ====/p' "$0" | head -n -1
}

# ── Dispatch ─────────────────────────────────────────────────
check_deps

case "${1:-help}" in
  gen-env)  cmd_gen_env ;;
  build)    cmd_build ;;
  up)       cmd_up ;;
  down)     cmd_down ;;
  reset)    cmd_reset ;;
  logs)     cmd_logs ;;
  status)   cmd_status ;;
  test)     cmd_test ;;
  shell)    cmd_shell "${2:-}" ;;
  help|--help|-h) cmd_help ;;
  *)        error "Unknown command: '${1}'. Run './manage.sh help' for usage." ;;
esac
