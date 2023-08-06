from offline_model_builder.user_profile.constants import CUSTOMER_ID, KMEANS_FEATURE, \
    MINIBATCH_KMEANS_FEATURE

ROOT_PATH = "../"
NON_FEATURES = [
    CUSTOMER_ID,
    MINIBATCH_KMEANS_FEATURE
    ]
NPZ_EXTENSION = ".npz"
CENTROIDS_IR1_PATH = "centroids_ir1"
EVAL_SCORES_IR2_PATH = "eval_scores_ir2"
INTER_CENTROID_SCORE_LABEL = "inter_centroid_distance"
BETWEEN_GROUP_SCATTER_LABEL = "between_group_scatter"
DUNN_INDEX_LABEL = "dunn_index"
BALLHALL_INDEX_LABEL = "ballhall_index"
LOGGING_BETWEENGROUPSCATTER = "Computing Between-Group Scatter..."
LOGGING_BALLHALLINDEX = "Computing Ball-Hall Index..."
LOGGING_DUNNINDEX = "Computing Dunn's Index..."
LOGGING_INTERCENTROIDDISTANCE = "Computing Inter-Centroid Distance..."