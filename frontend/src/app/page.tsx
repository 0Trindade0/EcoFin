"use client";

import { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";

interface Stock {
  id: number;
  symbol: string;
  name: string;
  price: number;
  change_percent: number;
  sector?: string | null;
  last_updated: string;
}

interface TaskStatus {
  task_id: string;
  status: string;
  result?: { updated?: boolean; reason?: string };
  error?: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
const wait = (milliseconds: number) =>
  new Promise((resolve) => setTimeout(resolve, milliseconds));

export default function Home() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [notice, setNotice] = useState("");
  const [formOpen, setFormOpen] = useState(false);
  const [saving, setSaving] = useState(false);
  const [refreshingSymbol, setRefreshingSymbol] = useState("");

  const fetchStocks = useCallback(async () => {
    setLoadError("");
    try {
      const response = await fetch(`${API_URL}/stocks/`);
      if (!response.ok) throw new Error("Não foi possível carregar os ativos.");
      setStocks(await response.json());
    } catch {
      setLoadError("Não foi possível conectar à API. Confira se o EcoFin está em execução.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void fetchStocks();
  }, [fetchStocks]);

  async function createStock(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setNotice("");
    setSaving(true);
    const form = event.currentTarget;
    const formData = new FormData(form);

    try {
      const response = await fetch(`${API_URL}/stocks/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          symbol: String(formData.get("symbol")).trim().toUpperCase(),
          name: String(formData.get("name")).trim(),
          sector: String(formData.get("sector")).trim() || null,
          price: 0,
        }),
      });
      const body = await response.json();
      if (!response.ok) throw new Error(body.detail ?? "Não foi possível cadastrar o ativo.");

      setFormOpen(false);
      setNotice(`${body.symbol} foi cadastrado. Solicitando a primeira cotação…`);
      form.reset();
      await fetchStocks();
      void refreshStock(body.symbol);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Erro ao cadastrar o ativo.");
    } finally {
      setSaving(false);
    }
  }

  async function refreshStock(symbol: string) {
    setNotice("");
    setRefreshingSymbol(symbol);
    try {
      const response = await fetch(`${API_URL}/stocks/${encodeURIComponent(symbol)}/refresh`, {
        method: "POST",
      });
      if (!response.ok) throw new Error("Não foi possível iniciar a atualização.");
      const { task_id: taskId } = await response.json();

      for (let attempt = 0; attempt < 45; attempt += 1) {
        await wait(2000);
        const statusResponse = await fetch(`${API_URL}/tasks/${taskId}`);
        if (!statusResponse.ok) throw new Error("Não foi possível consultar a atualização.");
        const task: TaskStatus = await statusResponse.json();

        if (task.status === "FAILURE") throw new Error(task.error ?? "A atualização falhou.");
        if (task.status === "SUCCESS") {
          await fetchStocks();
          setNotice(
            task.result?.updated === false
              ? `O provedor não retornou cotação para ${symbol}.`
              : `${symbol} foi atualizado.`,
          );
          return;
        }
      }
      setNotice(`A atualização de ${symbol} continua na fila. Atualize a lista em instantes.`);
    } catch (error) {
      setNotice(error instanceof Error ? error.message : "Erro ao atualizar o ativo.");
    } finally {
      setRefreshingSymbol("");
    }
  }

  return (
    <main className="min-h-screen bg-[#080b10] px-5 py-8 text-white sm:px-8">
      <div className="mx-auto max-w-6xl">
        <header className="mb-8 flex flex-wrap items-center justify-between gap-4 border-b border-white/10 pb-6">
          <div>
            <p className="mb-2 text-xs font-semibold uppercase tracking-[0.24em] text-emerald-400">EcoFin</p>
            <h1 className="text-3xl font-semibold tracking-tight sm:text-4xl">Sua carteira, em foco.</h1>
            <p className="mt-2 text-sm text-zinc-400">Cotações e variações dos ativos monitorados.</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={() => void fetchStocks()}
              className="rounded-lg border border-white/15 px-4 py-2.5 text-sm font-medium text-zinc-200 transition hover:bg-white/5"
            >
              Recarregar lista
            </button>
            <button
              onClick={() => { setNotice(""); setFormOpen(true); }}
              className="rounded-lg bg-emerald-400 px-4 py-2.5 text-sm font-semibold text-[#07110d] transition hover:bg-emerald-300"
            >
              + Adicionar ativo
            </button>
          </div>
        </header>

        {notice && <p role="status" className="mb-5 rounded-lg border border-white/10 bg-white/[0.04] px-4 py-3 text-sm text-zinc-200">{notice}</p>}
        {loadError && <p role="alert" className="mb-5 rounded-lg border border-red-400/20 bg-red-400/10 px-4 py-3 text-sm text-red-200">{loadError}</p>}

        {formOpen && (
          <form onSubmit={createStock} className="mb-8 grid gap-4 rounded-xl border border-white/10 bg-white/[0.035] p-5 sm:grid-cols-4">
            <div>
              <label htmlFor="symbol" className="mb-1.5 block text-xs text-zinc-400">Código</label>
              <input id="symbol" name="symbol" required maxLength={20} placeholder="PETR4.SA" className="w-full rounded-lg border border-white/10 bg-[#0b1017] px-3 py-2.5 text-sm outline-none focus:border-emerald-400" />
            </div>
            <div className="sm:col-span-2">
              <label htmlFor="name" className="mb-1.5 block text-xs text-zinc-400">Nome</label>
              <input id="name" name="name" required maxLength={120} placeholder="Petrobras PN" className="w-full rounded-lg border border-white/10 bg-[#0b1017] px-3 py-2.5 text-sm outline-none focus:border-emerald-400" />
            </div>
            <div>
              <label htmlFor="sector" className="mb-1.5 block text-xs text-zinc-400">Setor (opcional)</label>
              <input id="sector" name="sector" maxLength={80} placeholder="Energia" className="w-full rounded-lg border border-white/10 bg-[#0b1017] px-3 py-2.5 text-sm outline-none focus:border-emerald-400" />
            </div>
            <div className="flex gap-3 sm:col-span-4">
              <button disabled={saving} className="rounded-lg bg-emerald-400 px-4 py-2 text-sm font-semibold text-[#07110d] disabled:opacity-50">
                {saving ? "Cadastrando…" : "Cadastrar e buscar cotação"}
              </button>
              <button type="button" onClick={() => setFormOpen(false)} className="rounded-lg px-4 py-2 text-sm text-zinc-300 hover:bg-white/5">Cancelar</button>
            </div>
          </form>
        )}

        {loading ? (
          <p className="py-12 text-center text-sm text-zinc-500">Carregando ativos…</p>
        ) : stocks.length === 0 ? (
          <div className="rounded-xl border border-dashed border-white/15 px-6 py-16 text-center">
            <p className="text-lg font-medium">Sua lista ainda está vazia</p>
            <p className="mt-2 text-sm text-zinc-400">Cadastre um ativo para começar a acompanhar as cotações.</p>
          </div>
        ) : (
          <section aria-label="Ativos monitorados" className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
            {stocks.map((stock) => {
              const positive = stock.change_percent >= 0;
              return (
                <article key={stock.id} className="rounded-xl border border-white/10 bg-white/[0.035] p-5 transition hover:border-white/20">
                  <div className="mb-8 flex items-start justify-between gap-3">
                    <div>
                      <h2 className="text-xl font-semibold tracking-wide">{stock.symbol}</h2>
                      <p className="mt-1 text-sm text-zinc-400">{stock.name}</p>
                    </div>
                    <span className="max-w-32 truncate rounded-full border border-white/10 px-2.5 py-1 text-[10px] uppercase tracking-wider text-zinc-400">{stock.sector || "Sem setor"}</span>
                  </div>
                  <div className="flex items-end justify-between gap-2">
                    <div>
                      <p className="text-xs text-zinc-500">Último preço</p>
                      <p className="mt-1 text-3xl font-semibold tracking-tight">R$ {stock.price.toFixed(2).replace(".", ",")}</p>
                    </div>
                    <p className={`text-sm font-semibold ${positive ? "text-emerald-400" : "text-rose-400"}`}>
                      {positive ? "▲" : "▼"} {Math.abs(stock.change_percent).toFixed(2).replace(".", ",")}%
                    </p>
                  </div>
                  <div className="mt-5 flex items-center justify-between border-t border-white/10 pt-4">
                    <p className="text-xs text-zinc-500">
                      {stock.last_updated ? new Date(stock.last_updated).toLocaleString("pt-BR") : "Aguardando cotação"}
                    </p>
                    <button
                      onClick={() => void refreshStock(stock.symbol)}
                      disabled={Boolean(refreshingSymbol)}
                      className="text-xs font-medium text-emerald-300 transition hover:text-emerald-200 disabled:cursor-wait disabled:opacity-50"
                    >
                      {refreshingSymbol === stock.symbol ? "Atualizando…" : "Atualizar preço"}
                    </button>
                  </div>
                </article>
              );
            })}
          </section>
        )}
      </div>
    </main>
  );
}
