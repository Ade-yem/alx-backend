import { createClient } from 'redis';
import { promisify } from 'util';
const express = require('express');

const app = express();

const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 }
];

const getItemById = (id) => {
  return listProducts.find(product => product.id === id);
};

const client = createClient();
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

client.on('error', (error) => {
  console.error('Redis client not connected to the server:', error);
});

function reserveStockById (itemId, stock) {
  const key = `item.${itemId}`;
  client.set(key, stock);
}
async function getCurrentReservedStockById (itemId) {
  const key = `item.${itemId}`;
  const getAsync = promisify(client.get).bind(client);
  const res = await getAsync(key);
  return parseInt(res) || 0;
}

app.use(express.json());

app.get('/list_products', async (req, res) => {
  const result = listProducts.map(product => ({
    itemId: product.id, itemName: product.name, price: product.price, initialAvailableQuantity: product.stock
  }));
  res.json(result);
});

app.get('/list_products/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const product = getItemById(parseInt(itemId));
  const currentReservedStock = await getCurrentReservedStockById(parseInt(itemId));
  if (!product) res.json({ status: 'Product not found' });
  else {
    const result = {
      itemId: product.id,
      itemName: product.name,
      price: product.price,
      initialAvailableQuantity: product.stock,
      currentQuantity: product.stock - currentReservedStock
    };
    res.json(result);
  }
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const { itemId } = req.params;
  const item = getItemById(parseInt(itemId));
  if (!item) res.json({ status: 'Product not found' });
  else {
    const reservedStock = await getCurrentReservedStockById(itemId);
    const currentQuantity = item.stock - reservedStock;
    if (currentQuantity < 1) res.json({ status: 'Not enough stock available', itemId: itemId });
    else {
      reserveStockById(itemId, 1);
      res.json({ status: 'Reservation confirmed', itemId: itemId });
    }
  }
});

app.listen(1245, () => { console.log('Server is listening on port 1245'); });
