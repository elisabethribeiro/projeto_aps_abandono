function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu("Ações Clínicas")
    .addItem("Atualizar Status LC", "atualizarStatusAgenda")
    .addToUi();
}

function atualizarStatusAgenda() {
  const planilha = SpreadsheetApp.getActiveSpreadsheet();
  
  const abaAgenda = planilha.getSheetByName("agenda");
  const abaPendencias = planilha.getSheetByName("pendencias_gerais");
  
  if (!abaAgenda || !abaPendencias) {
    SpreadsheetApp.getUi().alert("Verifique se as abas 'agenda' e 'pendencias_gerais' existem com esses nomes.");
    return;
  }
  
  // 1. Carrega pendencias para a memória
  const dadosPendencias = abaPendencias.getDataRange().getValues();
  if (dadosPendencias.length <= 1) {
    SpreadsheetApp.getUi().alert("A aba 'pendencias_gerais' está vazia.");
    return;
  }
  
  const cabecalhoPendencias = dadosPendencias[0];
  const colIdPendencias = cabecalhoPendencias.indexOf("id_paciente");
  const colStatusLCPendencias = cabecalhoPendencias.indexOf("status_LC");
  
  if (colIdPendencias === -1 || colStatusLCPendencias === -1) {
    SpreadsheetApp.getUi().alert("Colunas 'id_paciente' ou 'status_LC' não encontradas em pendencias_gerais.");
    return;
  }
  
  // Cria mapa rápido de busca
  const mapaStatus = new Map();
  for (let i = 1; i < dadosPendencias.length; i++) {
    const id = String(dadosPendencias[i][colIdPendencias]).trim();
    const status = dadosPendencias[i][colStatusLCPendencias];
    if (id) {
      mapaStatus.set(id, status);
    }
  }
  
  // 2. Lê agenda
  const dadosAgenda = abaAgenda.getDataRange().getValues();
  if (dadosAgenda.length <= 1) {
    SpreadsheetApp.getUi().alert("A aba 'agenda' está vazia.");
    return;
  }
  
  const cabecalhoAgenda = dadosAgenda[0];
  const colIdAgenda = cabecalhoAgenda.indexOf("id_paciente");
  let colStatusAgenda = cabecalhoAgenda.indexOf("Status LC");
  
  if (colIdAgenda === -1) {
    SpreadsheetApp.getUi().alert("Coluna 'id_paciente' não encontrada na aba agenda.");
    return;
  }
  
  if (colStatusAgenda === -1) {
    colStatusAgenda = cabecalhoAgenda.length;
    abaAgenda.getRange(1, colStatusAgenda + 1).setValue("Status LC");
  }
  
  // 3. Monta lote de atualização
  const novasLinhas = [];
  for (let j = 1; j < dadosAgenda.length; j++) {
    const idAgenda = String(dadosAgenda[j][colIdAgenda]).trim();
    if (!idAgenda) {
      novasLinhas.push([""]);
      continue;
    }
    
    if (mapaStatus.has(idAgenda)) {
      novasLinhas.push([mapaStatus.get(idAgenda)]);
    } else {
      novasLinhas.push(["Não localizado"]);
    }
  }
  
  // 4. Grava em bloco na coluna
  abaAgenda.getRange(2, colStatusAgenda + 1, novasLinhas.length, 1).setValues(novasLinhas);
  
  SpreadsheetApp.getUi().alert("Status atualizados com sucesso!");
}
