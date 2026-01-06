"use client";

import { useEffect, useState } from "react";

interface Stock {
  id: number;
  symbol: string;
  name: string;
  price: number;
  change_percent: number; // Agora temos este dado!
  sector?: string;
}

export default function Home() {
  const [stocks, setStocks] = useState<Stock[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchStocks = async () => {
    try {
      const response = await fetch("http://localhost:8000/stocks/");
      if (response.ok) {
        const data = await response.json();
        setStocks(data);
      }
    } catch (error) {
      console.error("Erro de conexão:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStocks();
  }, []);

  return (
    <main className="min-h-screen bg-black text-white p-8">
      <header className="mb-10 flex justify-between items-center border-b border-zinc-800 pb-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">EcoFin Dashboard</h1>
          <p className="text-zinc-400 mt-1">Monitoramento em Tempo Real</p>
        </div>
        <button 
          onClick={fetchStocks}
          className="bg-blue-600 text-white px-5 py-2.5 rounded-lg font-medium hover:bg-blue-700 transition active:scale-95 flex items-center gap-2"
        >
          🔄 Atualizar
        </button>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading ? (
          <p className="text-zinc-500">Carregando...</p>
        ) : stocks.length === 0 ? (
          <p className="text-zinc-500">Nenhum ativo. Use o Swagger para adicionar.</p>
        ) : (
          stocks.map((stock) => {
            // Lógica de Cor
            const isPositive = stock.change_percent >= 0;
            const colorClass = isPositive ? "text-green-400" : "text-red-400";
            const arrow = isPositive ? "▲" : "▼";

            return (
              <div key={stock.id} className="bg-zinc-900 p-6 rounded-xl border border-zinc-800 hover:border-zinc-600 transition">
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h2 className="text-2xl font-bold">{stock.symbol}</h2>
                    <p className="text-sm text-zinc-400">{stock.name}</p>
                  </div>
                  <span className="bg-zinc-800 text-zinc-300 text-xs font-semibold px-2 py-1 rounded">
                    {stock.sector || "AÇÃO"}
                  </span>
                </div>
                <div className="flex justify-between items-end">
                  <span className="text-4xl font-bold tracking-tighter">
                    R$ {stock.price.toFixed(2).replace('.', ',')}
                  </span>
                  <div className="text-right">
                    <span className={`block font-bold text-lg ${colorClass}`}>
                      {arrow} {Math.abs(stock.change_percent).toFixed(2)}%
                    </span>
                    <span className="text-xs text-zinc-500">Última variação</span>
                  </div>
                </div>
              </div>
            );
          })
        )}
        
        {/* Placeholder Card */}
        <div className="bg-zinc-900/50 p-6 rounded-xl border border-dashed border-zinc-700 flex flex-col items-center justify-center text-zinc-500 hover:bg-zinc-900 hover:border-zinc-500 transition cursor-pointer group h-full min-h-[150px]">
          <div className="text-4xl mb-2 group-hover:text-zinc-300">+</div>
          <span className="group-hover:text-zinc-300">Adicionar Ativo</span>
        </div>
      </div>
    </main>
  );
}