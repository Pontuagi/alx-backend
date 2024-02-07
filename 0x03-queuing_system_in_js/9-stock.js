const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;

// Data
const listProducts = [
  { itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4 },
  { itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10 },
  { itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2 },
  { itemId: 4, itemName: 'Suitcase 1050', price: 550, initialAvailableQuantity: 5 }
];

// Data access
function getItemById (id) {
  return listProducts.find(product => product.itemId === id);
}

// Server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});

// Products Route
app.get('/list_products', (req, res) => {
  res.json(listProducts.map(product => ({
    itemId: product.itemId,
    itemName: product.itemName,
    price: product.price,
    initialAvailableQuantity: product.initialAvailableQuantity
  })));
});

// Redis Client
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Reserve Stock in Redis
async function reserveStockById (itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

async function getCurrentReservedStockById (itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock ? parseInt(stock) : 0;
}

// Product Detail Route
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    return res.json({ status: 'Product not found' });
  }
  const currentQuantity = await getCurrentReservedStockById(itemId);
  res.json({ ...product, currentQuantity });
});

// Reserve Product Route
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId);
  const product = getItemById(itemId);
  if (!product) {
    return res.json({ status: 'Product not found' });
  }
  const currentQuantity = await getCurrentReservedStockById(itemId);
  if (currentQuantity === 0) {
    return res.json({ status: 'Not enough stock available', itemId });
  }
  await reserveStockById(itemId, currentQuantity - 1);
  res.json({ status: 'Reservation confirmed', itemId });
});
