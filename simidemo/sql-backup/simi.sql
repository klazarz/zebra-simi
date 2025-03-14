--load model into DB
begin
   dbms_vector.drop_onnx_model(
      model_name => 'all_MiniLM_L12_v2',
      force      => true
   );
   dbms_vector.load_onnx_model(
      directory  => 'DEMO_PY_DIR',
      file_name  => 'all_MiniLM_L12_v2.onnx',
      model_name => 'demo_model'
   );
end;
/


-- create vector
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


--test query
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





 -- show also the distance

select p.prod_desc,
       p.prod_category_desc,
       p.prod_list_price,
       vector_distance(
          p.embedding,
          dbms_vector_chain.utl_to_embedding(
             'tennis',
             json(
                   '{"provider":"database", "model":"demo_model"}'
                )
          ),
          cosine
       ) as distance
  from products_vector p
 order by vector_distance(
   p.embedding,
   dbms_vector_chain.utl_to_embedding(
      'tennis',
      json(
            '{"provider":"database", "model":"demo_model"}'
         )
   ),
   cosine
)
 fetch first 4 rows only;



select *
  from products_vector;