"""Settings for the GNodeFactory, readable from environment and/or from env files."""

from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic import SecretStr


DEFAULT_ENV_FILE = ".env"


class GnfPublic(BaseModel):
    """This class is the publicly available information about the GNodeFactory"""

    algod_address: str = "http://localhost:4001"
    kmd_address: str = "http://localhost:4002"
    gen_kmd_wallet_name: str = "unencrypted-default-wallet"
    universe: str = "dev"
    gnf_g_node_alias: str = "dwgps.gnf"
    gnf_admin_addr: str = "RNMHG32VTIHTC7W3LZOEPTDGREL5IQGK46HKD3KBLZHYQUCAKLMT4G5ALI"
    gnf_graveyard_addr: str = (
        "COA6SYUOBE33F5JDYEGC5XAD43QRG3VGHNNQXLYWFSSQEHDQ5HJ52NDNPI"
    )
    gnr_addr: str = "X2ASUAUPK5ICMGDXQZQKBPSXWEJLBA4KKQ2TXW2KWO2JQTLY3J2Q4S33WE"
    gnf_validator_funding_threshold_algos: int = 100
    ta_deed_consideration_algos: int = 50
    gnf_api_root: str = "http://localhost:8000"
    molly_api_root: str = "http://localhost:8001"
    molly_cert_name: str = "Molly Metermaid"
    molly_name: str = "Molly Inc Telemetry Surveyors and Purveyors"
    keene_addr: str = "JMEUH2AXM6UGRJO2DBZXDOA2OMIWQFNQZ54LCVC4GQX6QDOX5Z6JRGMWFA"


class AlgoApiSecrets(BaseModel):
    algod_token: SecretStr = SecretStr(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    kmd_token: SecretStr = SecretStr(
        "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    )
    gen_kmd_wallet_password: SecretStr = SecretStr("")


class VanillaSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: GnfPublic = GnfPublic()

    class Config:
        env_prefix = "VANILLA_"
        env_nested_delimiter = "__"


class TaOwnerSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: GnfPublic = GnfPublic()
    sk: SecretStr = SecretStr(
        "sp4SDWmH8Rin0IhPJQq1UMsSR5C0j1IGqzLdcwCMySBVzT8lEUwjwwpS9z6l6dKSg52WWEjRdJDAL+eVt4kvBg=="
    )

    ta_daemon_addr: str = "NZXUSTZACPVJBHRSSJ5KE3JUPCITK5P2O4FE67NYPXRDVCJA6ZX4AL62EA"
    validator_addr: str = "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII"
    ta_daemon_api_fqdn: str = "http://localhost"
    ta_daemon_api_port: str = "8002"
    initial_ta_alias: str = "d1.isone.ver.keene.holly.ta"
    micro_lat: int = 45511230
    micro_lon: int = -68354650

    class Config:
        env_prefix = "HH_"
        env_nested_delimiter = "__"


class ValidatorSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: GnfPublic = GnfPublic()
    sk: SecretStr = SecretStr(
        "FCLmrvflibLD6Deu3NNiUQCC9LOWpXLsbMR/cP2oJzH8IT4Zu8vBAhRNsXoWF+2i6q2KyBZrPhmbDCKJD7rBBg=="
    )
    cert_name: str = "Molly Metermaid"
    name: str = "Molly Inc Telemetry Surveyors and Purveyors"
    api_root: str = "http://localhost:8001"

    class Config:
        env_prefix = "VLDTR_"
        env_nested_delimiter = "__"


class GnfSettings(BaseSettings):
    """Settings for the gNodeFactory."""

    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: GnfPublic = GnfPublic()
    g_node_alias: str = "dwgps.gnf"
    g_node_id: str = "ba1bd498-8bed-4a80-aa61-aa91e5f7d532"
    g_node_instance_id: str = "9fc843f3-ba36-46cc-990e-f45d3c02c210"
    log_level: str = "WARNING"
    admin_acct_sk: SecretStr = SecretStr(
        "qUGjVDcxVa0TfV8IeL8ZG9FFROh/GzLaWS6Ie05jrHiLWHNvVZoPMX7bXlxHzGaJF9RAyueOoe1BXk+IUEBS2Q=="
    )
    graveyard_acct_sk: SecretStr = SecretStr(
        "6UKcDTGYg7sU41D3si+VKBQSd5w46Z4mjVkahRfLIQETgelijgk3svUjwQwu3APm4RNupjtbC68WLKUCHHDp0w=="
    )
    # rabbit_url: SecretStr = SecretStr("amqp://smqPublic:smqPublic@localhost:5672/d1__1")
    rabbit_url: SecretStr = SecretStr(
        "amqp://smqPublic:smqPublic@d1-1.electricity.works:5672/d1__1"
    )
    rabbit_mqtt_port: int = 1885
    django_secret_key: str = "ai#6hnzekef0l^8f4x$uq*4j4im+hdcax0v^lxca4^#ozgnc+j"

    class Config:
        env_prefix = "GNF_"
        env_nested_delimiter = "__"


class TaDaemonSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: GnfPublic = GnfPublic()
    sk: SecretStr = SecretStr(
        "tQ8ABbLLR96cnRE3Y2tlrj2d/rNPRFkf8FosJ46tVIlub0lPIBPqkJ4yknqibTR4kTV1+ncKT324feI6iSD2bw=="
    )
    ta_owner_addr: str = "KXGT6JIRJQR4GCSS647KL2OSSKBZ3FSYJDIXJEGAF7TZLN4JF4DGDDX4BI"
    validator_addr: str = "7QQT4GN3ZPAQEFCNWF5BMF7NULVK3CWICZVT4GM3BQRISD52YEDLWJ4MII"

    class Config:
        env_prefix = "TAD_"
        env_nested_delimiter = "__"


class DiscovererSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: GnfPublic = GnfPublic()
    sk: SecretStr = SecretStr(
        "X20eXB/VZilEmzaPCDSn9WsuGZ5/f0+IxuEhfYfVtmZR9q5bcbjpBodPpiUCCkr0Xv11sKYxf08PnAKQFNtW3Q=="
    )
    discovered_ctn_alias = "d1.isone.ver.keene.pwrs"
    original_child_alias_list = ["d1.isone.ver.keene.holly"]
    micro_lat = 44838681
    micro_lon = -68705311


class GnrSettings(BaseSettings):
    algo_api_secrets: AlgoApiSecrets = AlgoApiSecrets()
    public: GnfPublic = GnfPublic()
    sk: SecretStr = SecretStr(
        "RvfbAEdn2ADe0pF7984ioBuLTnd+t46cITzcEbE5v2i+gSoCj1dQJhh3hmCgvlexErCDilQ1O9tKs7SYTXjadQ=="
    )

    class Config:
        env_prefix = "GNR_"
        env_nested_delimiter = "__"
