drop table products_vector;


create table products_vector
   as
      select p.prod_id,
             p.prod_name,
             p.prod_desc,
             p.prod_category_desc,
             p.prod_list_price,
             to_vector(dbms_vector_chain.utl_to_embedding(
                p.prod_desc,
                json(
                      '{"provider":"database", "model":"demo_model"}'
                   )
             )) as embedding
        from products p;



select p.prod_desc,
       p.prod_category_desc,
       p.prod_list_price
  from products_vector p
 order by vector_distance(
   p.embedding,
   dbms_vector_chain.utl_to_embedding(
      'blue ball',
      json(
            '{"provider":"database", "model":"demo_model"}'
         )
   ),
   cosine
)
 fetch first 4 rows only;