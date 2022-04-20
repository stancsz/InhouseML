from inhouseml import tfRunner

job = tfRunner(
    name="",
    features="",
    labels=""
)
job.get_dataset_describe()

# SQL stored procedures
"""
CREATE FUNCTION sqf_get_dataset_describe( table text, features text[], labels text[])
  RETURNS text
AS $$
    import inhouseml

    sqf = inhouseml.Flow(
        table=table,
        features=features,
        columns=labels
    )
    return sqf.get_dataset_describe()

$$ LANGUAGE plpython3u;
"""