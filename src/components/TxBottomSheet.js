import React from "react";
import { Modal, Pressable, StyleSheet, Text, View, FlatList } from "react-native";
import { colors } from "../theme/colors";
import { radius } from "../theme/radius";

export default function TxBottomSheet({ visible, title, items, onClose, onSelect }) {
  return (
    <Modal transparent visible={visible} animationType="fade" onRequestClose={onClose}>
      <Pressable style={styles.backdrop} onPress={onClose}>
        <Pressable style={styles.sheet} onPress={() => {}}>
          <View style={styles.header}>
            <Text style={styles.title}>{title}</Text>
            <Pressable onPress={onClose} style={styles.closeBtn}>
              <Text style={styles.closeText}>✕</Text>
            </Pressable>
          </View>

          <FlatList
            data={items}
            keyExtractor={(item) => String(item)}
            ItemSeparatorComponent={() => <View style={styles.sep} />}
            renderItem={({ item }) => (
              <Pressable
                onPress={() => onSelect(item)}
                style={({ pressed }) => [styles.row, pressed && { opacity: 0.85 }]}
              >
                <Text style={styles.rowText}>{item}</Text>
              </Pressable>
            )}
          />
        </Pressable>
      </Pressable>
    </Modal>
  );
}

const styles = StyleSheet.create({
  backdrop: {
    flex: 1,
    backgroundColor: "rgba(0,0,0,0.25)",
    justifyContent: "flex-end",
  },
  sheet: {
    backgroundColor: "#fff",
    borderTopLeftRadius: radius.xl,
    borderTopRightRadius: radius.xl,
    padding: 16,
    maxHeight: "70%",
  },
  header: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginBottom: 10 },
  title: { fontSize: 16, fontWeight: "900", color: colors.textPrimary },
  closeBtn: { padding: 8 },
  closeText: { fontSize: 18, fontWeight: "900", color: "#9CA3AF" },
  sep: { height: 1, backgroundColor: colors.border },
  row: { paddingVertical: 14 },
  rowText: { fontSize: 15, fontWeight: "800", color: colors.textPrimary },
});
