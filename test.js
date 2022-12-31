new gridjs.Grid({
columns: [
  { id: 'date_open', name: 'Date' },
  { id: 'status', name: 'Status' },
  { id: 'symbol', name: 'Symbol' },
  { id: 'qty', name: 'Quantity' },
  { id: 'cost_basis', name: 'Cost Basis' },
  { id: 'net_cost', name: 'Net Cost' },
  { id: 'notes', name: 'Notes' },
  { id: 'img', name: 'Image' },
],
data: [
    {
      date_open: '{{ position.date_open }}',
      status: {{ position.status }},
      symbol: '{{ position.symbol }}',
      qty: '{{ position.qty }}',
      cost_basis: '{{ position.cost_basis }}',
      net_cost: '{{ position.net_cost }}',
      notes: '{{ position.notes }}',
      img: '{{ position.img }}',
    },
],
search: true,
sort: true,
pagination: false,
}).render(document.getElementById('table'));
