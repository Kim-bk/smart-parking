package com.parkingsmart.repository;

import java.util.List;

import org.springframework.data.jpa.repository.JpaRepository;

import com.parkingsmart.entity.DistrictEntity;
import com.parkingsmart.entity.WardEntity;

public interface WardRepository extends JpaRepository<WardEntity, String> {
	List<WardEntity> findByDistrict(DistrictEntity district);
}
