DELETE FROM orders USING (
      SELECT MIN(ctid) as ctid, id
        FROM orders 
        GROUP BY id HAVING COUNT(*) > 1
      ) dups
      WHERE orders.id = dups.id 
      AND orders.ctid <> dups.ctid
