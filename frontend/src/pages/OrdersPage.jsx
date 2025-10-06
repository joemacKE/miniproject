import React, { useEffect, useState } from "react";
import axiosClient from "../api/axiosClient";

const OrdersPage = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    axiosClient
      .get("orders/list/") // matches your Django endpoint
      .then((response) => {
        setOrders(response.data);
      })
      .catch((error) => {
        console.error("Error fetching orders:", error);
      });
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-4">Orders</h2>
      {orders.length > 0 ? (
        <ul className="space-y-2">
          {orders.map((order) => (
            <li key={order.id} className="border p-4 rounded-lg shadow-sm">
              <p>
                <strong>Title:</strong> {order.title}
              </p>
              <p>
                <strong>Status:</strong> {order.status}
              </p>
              <p>
                <strong>Pages:</strong> {order.pages}
              </p>
            </li>
          ))}
        </ul>
      ) : (
        <p>No orders found.</p>
      )}
    </div>
  );
};

export default OrdersPage;
