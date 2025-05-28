def sort_list_by_another_list_order(target_list, order_list):
	"""
	target_list を order_list の順序に従って並べ替えます。
	order_list に含まれない target_list の要素は、
	元の相対順序を保ったまま末尾に配置されます。

	Args:
		target_list (list): 並べ替えたいリスト。
		order_list (list): 基準となる順序を持つリスト。
						   このリストの要素はユニークであることが期待されます。
						   重複がある場合、最初の出現位置が優先されます。

	Returns:
		list: 並べ替えられた新しいリスト。
	"""
	# order_list の要素とそのインデックスをマッピングする辞書を作成
	# これにより、各要素の順序を O(1) で検索できるようになります。
	# order_list に重複があった場合、最初の出現インデックスを優先します。
	order_map = {}
	for i, item in enumerate(order_list):
		if item not in order_map:
			order_map[item] = i

	# 元のリストのインデックスを保持するために (original_index, item) のタプルのリストを作成
	# これにより、ソートキーが同じ要素間の元の順序を維持できます（安定ソート）。
	indexed_target_list = list(enumerate(target_list))

	def sort_key(indexed_item):
		original_index, item = indexed_item
		if item in order_map:
			# グループ0: order_list に存在する要素
			# ソートキー: (グループ識別子, order_list内での順序, 元のインデックス)
			# 元のインデックスをキーの最後に含めることで、
			# order_map[item] が同じ値を持つ要素間の安定性を保証します。
			return (0, order_map[item], original_index)
		else:
			# グループ1: order_list に存在しない要素
			# ソートキー: (グループ識別子, 元のインデックス)
			# これにより、order_list にない要素は全てグループ0の要素の後に来て、
			# その中では元の相対順序が保たれます。
			return (1, original_index)

	# カスタムキーを使ってソート
	sorted_indexed_list = sorted(indexed_target_list, key=sort_key)

	# タプルのリストから要素のみを抽出して新しいリストを作成
	result_list = [item for original_index, item in sorted_indexed_list]
	return result_list

def reorder_dict_with_remaining(original_dict, key_order_list):
	"""
	指定されたキーリストの順序で辞書を再構築し、
	その後、キーリストに含まれていなかった元の辞書のキーを（元の順序で）追加します。

	Args:
		original_dict (dict): 元の辞書。
		key_order_list (list): 望ましいキーの順序を指定するリスト。

	Returns:
		dict: 再順序付けされた新しい辞書。
	"""
	reordered_dict = {}
	processed_keys = set() # 既に追加されたキーを追跡するためのセット

	# 1. key_order_list に従ってキーを追加
	for key in key_order_list:
		if key in original_dict:
			reordered_dict[key] = original_dict[key]
			processed_keys.add(key)

	# 2. 元の辞書に残っているキーを（元の挿入順で）追加
	for key, value in original_dict.items():
		if key not in processed_keys:
			reordered_dict[key] = value

	return reordered_dict
