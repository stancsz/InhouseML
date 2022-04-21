CREATE EXTENSION plpython3u;

CREATE FUNCTION ml_dataset_describe(name text, features text[], labels text[])
    RETURNS JSON
AS
$$
   from inhouseml import tfRunner
   job = tfRunner(name=name, features=features, labels=labels)
   job.load_dataset(plpy.execute(job.get_query()))
   return job.get_dataset_describe()
$$ LANGUAGE plpython3u;

CREATE FUNCTION ml_train_dnn(name text, features text[], labels text[])
    RETURNS JSON
AS
$$
   from inhouseml import tfRunner
   job = tfRunner(name=name, features=features, labels=labels)
   job.load_dataset(plpy.execute(job.get_query()))
   info = job.train_dnn(name)
   return info
$$ LANGUAGE plpython3u;